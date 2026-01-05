from collections import defaultdict
from datetime import date, timedelta

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models

MONTHS = {
    '01': 'Enero',
    '02': 'Febrero',
    '03': 'Marzo',
    '04': 'Abril',
    '05': 'Mayo',
    '06': 'Junio',
    '07': 'Julio',
    '08': 'Agosto',
    '09': 'Septiembre',
    '10': 'Octubre',
    '11': 'Noviembre',
    '12': 'Diciembre',
}


class ProductProduct(models.Model):
    _inherit = "product.product"

    sales_last_months = fields.Html(
        string="Ventas últimos meses",
        compute="_compute_sales_last_months",
        store=True
    )

    purchase_last_months = fields.Html(
        string="Compras últimos meses",
        compute="_compute_purchase_last_months",
        store=True
    )

    last_sale_of_month = fields.Char(
        string="Mes actual",
        compute="_compute_last_sale_of_month",
        store=True
    )


    def action_view_stock_moves(self):
        self.ensure_one()
        date_from = fields.Datetime.now() - relativedelta(days=365)

        return {
            'name': 'Movimientos de Stock',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.move.line',
            'view_mode': 'list',
            'domain': [
                ('product_id', '=', self.id),
                ('state', '=', 'done'),
                ('date', '>=', date_from),
            ],
            'target': 'current',
        }

    def action_open_sales_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Resumen de Producto',
            'res_model': 'product.sales.summary',
            'view_mode': 'form',
            'view_id': self.env.ref('opentech_inventory_extensions.view_product_sales_summary_form').id,
            'target': 'new',
            'context': {
                'default_product_id': self.id,
            },
        }

    @api.depends('stock_move_ids.state', 'stock_move_ids.date', 'stock_move_ids.product_id')
    def _compute_sales_last_months(self):
        today = date.today()
        start_date = (today.replace(day=1) - timedelta(days=180)).replace(day=1)

        for product in self:
            move_lines = self.env['stock.move.line'].search([
                ('product_id', '=', product.id),
                ('state', '=', 'done'),
                ('date', '>=', start_date),
                ('picking_id.picking_type_code', '=', 'outgoing'),
            ])
            sales_by_month = {}
            for line in move_lines:
                month_str = line.date.strftime('%m')
                if month_str not in sales_by_month:
                    sales_by_month[month_str] = 0
                sales_by_month[month_str] += line.quantity

            product.sales_last_months = self._render_month_dict_html(
                sales_by_month,
                title="Ventas últimos meses",
                accent="#198754",
                icon="fa-arrow-up-right"
            )

    @api.depends('stock_move_ids.state', 'stock_move_ids.date', 'stock_move_ids.product_id')
    def _compute_purchase_last_months(self):
        today = date.today()
        start_date = (today.replace(day=1) - timedelta(days=180)).replace(day=1)

        for product in self:
            move_lines = self.env['stock.move.line'].search([
                ('product_id', '=', product.id),
                ('state', '=', 'done'),
                ('date', '>=', start_date),
                ('picking_id.picking_type_code', '=', 'incoming'),
            ])
            purchase_by_month = {}
            for line in move_lines:
                month_str = line.date.strftime('%m')
                if month_str not in purchase_by_month:
                    purchase_by_month[month_str] = 0
                purchase_by_month[month_str] += line.quantity

            product.purchase_last_months = self._render_month_dict_html(
                purchase_by_month,
                title="Compras últimos meses",
                accent="#0d6efd",
                icon="fa-arrow-down"
            )

    @api.depends('stock_move_ids.state', 'stock_move_ids.date', 'stock_move_ids.product_id')
    def _compute_last_sale_of_month(self):

        now = fields.Datetime.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        for product in self:

            move_lines = self.env['stock.move.line'].search([
                ('product_id', '=', product.id),
                ('state', '=', 'done'),
                ('date', '>=', month_start),
                ('picking_id.picking_type_code', '=', 'outgoing'),
            ])

            last_sale_of_month = {}
            for line in move_lines:
                month_str = line.date.strftime('%m')
                if month_str not in last_sale_of_month:
                    last_sale_of_month[month_str] = 0
                last_sale_of_month[month_str] += line.quantity

            sales_str = "\n".join([f"{MONTHS[month]}: {qty}" for month, qty in last_sale_of_month.items()])
            product.last_sale_of_month = sales_str

    def _render_month_dict_html(self, data_dict, title, accent="#0d6efd", icon="fa-bar-chart"):
        """
        data_dict: {Mes: cantidad}
        title:     título de la tarjeta
        accent:    color de acento (hex)
        icon:      icono FA opcional
        """
        rows = []
        total = 0.0
        max_qty = max(data_dict.values()) if data_dict else 0.0

        for m in data_dict.keys():
            qty = data_dict[m] or 0.0
            total += qty
            width = 0 if max_qty <= 0 else int((qty / max_qty) * 100)
            rows.append(f"""
                <tr>
                    <td class="pp-month">{MONTHS[m]}</td>
                    <td></td>
                    <td class="pp-qty">{qty:g}</td>
                    <td class="pp-bar">
                        <div class="pp-bar-track">
                            <div class="pp-bar-fill" style="width:{width}%"></div>
                        </div>
                    </td>
                </tr>
            """)

        if not rows:
            rows_html = """<tr><td colspan="3" class="pp-empty">Sin datos en el período</td></tr>"""
        else:
            rows_html = "\n".join(rows)

        # HTML + estilos inline (auto-contenido, sin depender de assets)
        html = f"""
        <div class="pp-card">
            <div class="pp-card-header">
                <i class="fa {icon}" style="margin-right:.5rem;"></i>{title}
            </div>
            <div class="pp-card-body">
                <table class="pp-table">
                    <thead>
                        <tr>
                            <th>Mes</th>
                            <th>
                            <th>Cant.</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
            </div>
        </div>
        <style>
            .pp-card {{
                border: 1px solid #e6e6e6; border-radius: 12px; overflow: hidden;
                box-shadow: 0 1px 2px rgba(0,0,0,.04);
            }}
            .pp-card-header {{
                background: {accent}10; color: #333; font-weight: 600; padding: .75rem 1rem;
                border-bottom: 1px solid #eee;
            }}
            .pp-card-body {{ padding: .5rem 1rem 1rem 1rem; }}
            .pp-table {{ width: 100%; border-collapse: separate; font-size: 13px; }}
            .pp-table thead th {{
                text-align: left; padding: .5rem; border-bottom: 1px solid #eee; color:#555;
            }}
            .pp-table td {{ padding: .4rem .5rem; vertical-align: middle; }}
            .pp-month {{ white-space: nowrap; }}
            .pp-qty {{ font-variant-numeric: tabular-nums; font-weight: 600; }}
            .pp-bar-track {{
                width: 100%; height: 8px; background: #f2f2f2; border-radius: 999px; overflow: hidden;
            }}
            .pp-bar-fill {{
                height: 100%; background: {accent}; opacity:.9;
            }}
            .pp-total-label {{ font-weight: 700; }}
            .pp-total-value {{ font-weight: 700; }}
            .pp-empty {{ color:#999; text-align:center; padding:.75rem; }}
        </style>
        """
        return html
