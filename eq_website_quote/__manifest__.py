# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Equitania Website Angebote',
    'license': 'AGPL-3',
    'version': '1.0.2',
    'description': """
        Improvement of website_quote
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup', 'sale', 'eq_sale', 'eq_base_report', 'website_quote'],
    'category' : 'Website',
    'summary': 'Improvement of website_quote',

    'data': [
        "views/templates.xml",

    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
