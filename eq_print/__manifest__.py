# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Equitania Printing',
    'version': '1.0.2',
    'summary': """
        Modul um PDF's sofort auszudrucken
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base', 'base_setup'],
    'category' : 'tools',
    'description': """
     Modul um PDF's sofort auszudrucken
    """,
    'data': [
        'security/ir.model.access.csv',
        'wizard/eq_print_wiz_view.xml',
        'views/eq_spooltable_view.xml',
        'views/eq_printer_view.xml',
        'views/res_users_view.xml',
        'views/ir_actions_report_xml_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
