{
    'name': "Opentech Inventory Extensions",
    'version': '18.0.1.0.0',
    'summary': "Extensiones de inventario para productos y stock en Odoo 18",
    'description': """
        Extensiones sobre modelos relacionados con inventario.
        Botón en vistas tree de product.template y product.product para abrir stock.move.line hechos.
        """,
    'author': 'Opentech',
    'category': 'Inventory',
    'license': 'LGPL-3',
    'depends': ['stock', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/product_product_sales_history_view.xml',
        'views/product_product_views.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
}
