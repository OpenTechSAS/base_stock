{
    'name': "OpenTech Inventory Extensions",
    'description': """
        Este módulo añade funcionalidades personalizadas al módulo de inventario (stock),
    """,
    'author': "OpenTech",
    'version': '18.0.1.0.0',
    'category': 'Inventory',
    "depends": [
        "base",
        "sale_management",
        "stock",
        'l10n_uy_edi_cfe',
    ],
    'data': [
        'security/ir.model.access.csv',
        "wizard/picking_invoice_wizard_views.xml",
        "views/stock_picking_views.xml",
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
