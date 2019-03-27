# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Equitania Access Rights",
    'license': 'AGPL-3',
    'version': '1.0.0',
    'category': 'access_rights',
    'description': """ Improved access rights for hr_holidays, hr_timesheet and hr_expense""",
    'author': 'Equitania Software GmbH',
    'summary': 'Access rights only to modules set up in settings depending on User/Manger group',
    'website': 'www.myodoo.de',
    "depends" : ['base', 'base_setup', 'hr_holidays', 'hr_timesheet', 'hr_expense'],
    'data': [
            'views/eq_hr_holidays_menu_item_view.xml',
            'views/eq_hr_timesheet_menu_item_view.xml',
            'views/eq_hr_expense_menu_item_view.xml',
             ],
    "active": False,
    "installable": True
}
