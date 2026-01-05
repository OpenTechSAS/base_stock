import calendar
import logging
import time
from datetime import date, datetime, timedelta

from odoo import fields, models

_logger = logging.getLogger(__name__)


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    def _get_days_buffer(self):
        """Obtiene los dias que seteo el cliente para borrar adjuntos viejos"""
        config = self.env['ir.config_parameter'].sudo()
        days_to_clean = int(config.get_param('l10n_uy_edi_cfe.days_to_clean'))

        if not days_to_clean:
            _logger.error("Falta la configuración de los días para limpiar CFEs en settings.")

        return days_to_clean

    def _sql_delete_range(self, day, batch_size=1000):
        Att = self.sudo()
        total = 0
        while True:
            day_start = datetime.combine(day, datetime.min.time())
            day_end = day_start + timedelta(days=1)

            self.env.cr.execute("""
                SELECT a.id
                FROM ir_attachment a
                WHERE a.type = 'binary'
                AND a.mimetype = 'application/pdf'
                AND a.res_id IS NOT NULL
                AND a.res_model IN (
                    'account.move',
                    'account.edi.format',
                    'gift_receipt_pos_sale_product'
                )
                AND (a.create_date - INTERVAL '3 hours') >= %s
                AND (a.create_date - INTERVAL '3 hours') <  %s
                ORDER BY a.id
                LIMIT %s
            """, (day_start, day_end, batch_size))
            ids = [r[0] for r in self.env.cr.fetchall()]
            if not ids:
                break
            Att.browse(ids).unlink()  # borra DB + archivo del filestore
            self.env.cr.commit()
            total += len(ids)
        return total

    def _month_ranges_until_cutoff(self):
        """Calculamos los días de borrado (solo fechas)"""
        days_buffer = self._get_days_buffer()
        if not days_buffer:
            return []

        cutoff = fields.Datetime.now() - timedelta(days=days_buffer)
        year = cutoff.year

        start_dt = datetime(year, 1, 1)
        end_dt = datetime(year, cutoff.month, cutoff.day)

        days = []
        current = start_dt
        while current <= end_dt:
            days.append(current.date())
            current += timedelta(days=1)
        return days

    def delete_old_attachments(self):
        """Borra los adjuntos de CFEs viejos"""
        days = self._month_ranges_until_cutoff() or []
        start_ts = time.time()

        for day in days:
            elapsed = time.time() - start_ts
            if elapsed >= 800:
                _logger.info("Límite de tiempo alcanzado, deteniendo la limpieza de adjuntos.")
                return
            _logger.info(f"Eliminando los adjuntos del dia {day}")
            self._sql_delete_range(day)
