from dateutil.relativedelta import relativedelta
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_view_stock_moves(self):
        self.ensure_one()
        date_from = fields.Datetime.now() - relativedelta(days=365)

        return {
            'name': 'Movimientos de Stock',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.move.line',
            'view_mode': 'list',
            'domain': [
                ('product_id', 'in', self.product_variant_ids.ids),
                ('state', '=', 'done'),
                ('date', '>=', date_from),
            ],
            'target': 'current',
        }
