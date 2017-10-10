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
    'name': 'Equitania Printing',
    'version': '1.0.1',
    'summary': """
        Equitania Printing
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base', 'base_setup'],
    'category' : 'tools',
    'description': """
     
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
