# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Equitania Module Template',
    'license': 'AGPL-3',
    'version': '1.0.1',
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup'],
    'category' : 'General Improvements',
    'summary': 'Module Template',

    'data': [
        #"security/ir.model.access.csv"
        "views/templates.xml",

    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
