# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Equitania Basis',
    'license': 'AGPL-3',
    'version': '1.0.12',
    'description': """
        Basic fields for more EQ Modules
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup', 'base'],
    'category' : 'General Improvements',
    'summary': 'Base extension',

    'data': [
         "views/res_company_view.xml",
         "views/res_country_view.xml",
         "views/eq_res_users_view.xml",
         "views/templates.xml",

    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
