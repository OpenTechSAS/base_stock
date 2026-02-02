from odoo import fields, models
from odoo.exceptions import UserError


class PickingInvoiceWizard(models.TransientModel):
    _name = 'picking.invoice.wizard'
    _description = 'Wizard para crear factura desde Picking'

    advance_payment_method = fields.Selection(
        selection=[
            ('posted', "Crear factura y confirmar"),
            ('draft', "Crear factura en borrador"),
        ],
        string="Create Invoice",
        required=True
    )

    picking_id = fields.Many2one('stock.picking', 
        string="Picking", 
        required=True,
        default=lambda self: self.env.context.get('default_picking_id')
    )

    def action_confirm(self):
        self.ensure_one()
        picking = self.picking_id

        sale = picking.sale_id
        if not sale:
            raise UserError("No hay orden de venta relacionada para crear la factura.")
        if sale.invoice_ids:
            raise UserError("La orden de venta ya tiene facturas creadas.")
        try:
            advance_payment_wizard = self.env['sale.advance.payment.inv'].with_context(
                active_model='sale.order',
                active_ids=[sale.id],
            ).create({
                'advance_payment_method': 'delivered',
            })
            invoice = advance_payment_wizard._create_invoices(sale)
            if self.advance_payment_method == 'posted':
                if invoice.partner_id.l10n_latam_identification_type_id.id != \
                    self.env.ref('l10n_uy.it_rut').id:
                    invoice._onchange_partner_id()
                invoice.action_post()
        except Exception as e:
            raise UserError(f"Error al crear la factura: {str(e)}")

        return picking.action_open_invoice()
