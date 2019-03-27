# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Equitania Stock Putaway Product',
    'license': 'AGPL-3',
    'version': '1.0.0',
    'description': """
        Extend OCA module stock_putaway_product
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup','stock_putaway_product'],
    'category' : 'General Improvements',
    'summary': 'Extend OCA module stock_putaway_product',

    'data': [
        #"security/ir.model.access.csv"
        #"views/templates.xml",

    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
