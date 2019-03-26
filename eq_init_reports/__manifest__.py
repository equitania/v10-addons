# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Reportsettings QWeb',
    'license': 'AGPL-3',
    'version': '1.0.6',
    'description': """
    Reporteinstellungen
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup', 'eq_account', 'eq_purchase', 'eq_sale', 'eq_stock'],
    'category' : 'General Improvements',
    'summary': 'Reporteinstellungen für QWeb',
    'data': [
        "security/ir.model.access.csv",
        "data/set_defaults.xml",
    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
