# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Equitania Personalwesen Optimierungen',
    'license': 'AGPL-3',
    'version': '1.0.11',
    'description': """
        Extensions for HR
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup', 'base', 'hr', 'hr_expense', 'hr_holidays', 'calendar'],
    'category': 'hr',
    'summary': 'HR Extensions',

    'data': [
        "views/eq_res_users_view.xml",
        "views/eq_hr_expense_view.xml",
        "views/eq_hr_holidays.xml",
        "views/eq_hr_holidays_view.xml",
        "views/eq_report_expense_sheet_sequence.xml",
        "views/eq_report_expense_sheet.xml",
        "security/eq_replace_calendar.xml",
        "security/eq_calendar_security.xml",

    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
