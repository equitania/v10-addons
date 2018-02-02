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
    'name': "Equitania Projekt",
    'license': 'AGPL-3',
    'version': '1.0.2',
    'category': 'project',
    'description': """Extensions for project""",
    'author': 'Equitania Software GmbH',
    'summary': 'Project Extension',
    'website': 'www.myodoo.de',
    "depends" : ['base','project','project_issue','hr_timesheet_activity_begin_end', 'analytic','project_parent',],  #no dependencies for stage was always in Project/Data/project_data.xml declared
    'data': [
            'data/ir_sequence_data.xml',
            'views/eq_project_extension_view.xml',
            'views/eq_issues_extension.xml',
             ],
    "active": False,
    "installable": True
}
