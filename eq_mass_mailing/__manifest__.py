# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Equitania Mass Mailing',
    'license': 'AGPL-3',
    'version': '1.0.0',
    'description': """
        Mass Mailing Module
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup','mass_mailing'],
    'category' : 'General Improvements',
    'summary': 'Mass Mailing',

    'data': [
        "data/newsletter.xml",

    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
