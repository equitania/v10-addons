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
    'name': 'Equitania HR Timesheet Begin End Erweiterungen',
    'license': 'AGPL-3',
    'version': '1.0.1',
    'description': """
        Equitania Erweiterungen für das HR Timesheet Begin End Modul der OCA
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['hr_timesheet_activity_begin_end'],
    'category' : 'Human Resources',
    'summary': 'Equitania HR Timesheet Begin End Erweiterungen',

    'data': [
        #"security/ir.model.access.csv"
        "views/eq_hr_analytic_timesheet.xml",

    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
