from odoo import fields, models


class ProductSalesSummary(models.TransientModel):
    _name = 'product.sales.summary'
    _description = 'Resumen de Ventas y Stock de un Producto'

    product_id = fields.Many2one(
        'product.product',
        string="Producto",
        required=True,
        readonly=True
    )

    image_1920 = fields.Image(related="product_id.image_1920", readonly=True)
    default_code = fields.Char(related="product_id.default_code", readonly=True)
    categ_id = fields.Many2one(related="product_id.categ_id", readonly=True)
    qty_available = fields.Float(related="product_id.qty_available", readonly=True)

    sales_last_months = fields.Html(
        string="Ventas últimos 6 meses",
        related="product_id.sales_last_months",
        readonly=True
    )

    purchase_last_months = fields.Html(
        string="Compras últimos 6 meses",
        related="product_id.purchase_last_months",
        readonly=True
    )

    lst_price = fields.Float(
        string="Precio de venta",
        related="product_id.lst_price",
        readonly=True,
    )

    tax_string = fields.Char(
        string="Precio imp. incl.",
        related="product_id.tax_string",
        readonly=True
    )

    last_sale_of_month = fields.Char(
        string="Mes actual",
        related="product_id.last_sale_of_month",
        readonly=True
    )
