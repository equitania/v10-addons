# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo Addon, Open Source Management Solution
#    Copyright (C) 2014-now Equitania Software GmbH(<http://www.equitania.de>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

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
