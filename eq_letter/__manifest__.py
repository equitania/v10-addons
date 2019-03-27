# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Equitania Letter',
    'license': 'AGPL-3',
    'version': '1.0.3',
    'description': """
        Equitania Letter
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup', 'web', 'web_planner'],
    'category' : 'General Improvements',
    'summary': 'Möglichkeit einen Brief in der Odoo Umgebung zu schreiben',

    'data': [
        "security/ir.model.access.csv",
        "views/eq_letter_view.xml",
        "views/eq_letter_report.xml",
        "views/eq_report_show.xml",

    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
