# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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
