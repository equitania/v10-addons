# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Equitania Einkauf Freie Positionen',
    'license': 'AGPL-3',
    'version': '1.0.1',
    'description': """
        Freie Positionen im Einkauf
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup','eq_purchase'],
    'category' : 'General Improvements',
    'summary': 'Freie Positionen im Einkauf',

    'data': [
        #"security/ir.model.access.csv"
        'views/eq_purchase_view.xml',

    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
