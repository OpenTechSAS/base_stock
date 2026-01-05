# -*- coding: utf-8 -*-
{
    'name': "Uruguayan docs validators",

    'summary': """
        Validate RUT and C.I.
        """,

    "license": "LGPL-3",
    'description': """
    Validate RUT and C.I.
    """,

    'author': "Grupo YACCK",
    'website': "www.grupoyacck.com",


    'category': 'Localization/Base',
    'version': '0.3',

    'depends': [
        'base',
        'l10n_uy',
    ],

    'data': [
        'views/res_partner_view.xml',
    ],
}