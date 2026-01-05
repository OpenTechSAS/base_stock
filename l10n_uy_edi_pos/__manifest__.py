# -*- coding: utf-8 -*-
{
    'name': "Uruguayan EDI POS",

    'summary': """
        POS, Uruguayan EDI""",

    'description': """
        POS, Uruguayan EDI
    """,

    "license": "LGPL-3",
    'author': "Grupo YACCK",
    'website': "http://www.grupoyacck.com",
    'category': 'Sales/Point of Sale',
    'version': '0.3',
    'depends': [
        'account',
        'l10n_uy_edi_cfe',
        'point_of_sale',
        'pos_qz_printing_mobile'
    ],
    'data': [
        # 'views/res_config_settings_views.xml',
    ],
    'assets': {
            'point_of_sale._assets_pos': [
                # 'l10n_uy_edi_pos/static/src/overrides/models/partner_editor.js',
                'l10n_uy_edi_pos/static/src/overrides/models/pos_order.js',
                # 'l10n_uy_edi_pos/static/src/overrides/models/pos_store.js',
                'l10n_uy_edi_pos/static/src/overrides/models/payment_screen.js',
                'l10n_uy_edi_pos/static/src/overrides/models/receipt_screen.js',
                'l10n_uy_edi_pos/static/src/overrides/models/ticket_screen.js',
                'l10n_uy_edi_pos/static/src/overrides/qz_printer/qz_local_printer.js',
                'l10n_uy_edi_pos/static/src/overrides/store/pos_store.js',
                #'l10n_uy_edi_pos/static/src/overrides/components/partner_editor/partner_editor.xml',
                'l10n_uy_edi_pos/static/src/overrides/components/receipt/order_receipt.xml',
                "l10n_uy_edi_pos/static/src/overrides/components/ticket_screens/ticket_screens.js",
            ],
    },
}
