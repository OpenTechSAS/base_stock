from odoo import fields, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_open_invoice(self):
        self.ensure_one()
        invoices = self.sale_id.invoice_ids
        invoice = False
        credit_note = False

        if len(invoices) > 3:
            return {
                'name': 'Factura',
                'type': 'ir.actions.act_window',
                'view_mode': 'list',
                'res_model': 'account.move',
                'domain': [('id', 'in', invoices.ids)],
            }

        for inv in invoices:
            if inv.move_type == 'out_refund':
                credit_note  = inv
            if inv.move_type == 'out_invoice':
                invoice  = inv

        if self.picking_type_code == 'incoming' and credit_note:
            return {
                'name': 'Nota de Crédito',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'account.move',
                'res_id': credit_note.id,
            }

        if self.picking_type_code == 'outgoing' and invoice:
            return {
                'name': 'Factura',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'account.move',
                'res_id': invoice.id,
            }

        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sin factura',
                    'message': 'No se encontró una factura asociada.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
