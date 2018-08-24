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
    'name': 'Equitania Mitarbeiterdokumente',
    'license': 'AGPL-3',
    'version': '1.0.6',
    'description': """
        Extensions for module oh_employee_documents_expiry
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup', 'base', 'hr', 'oh_employee_documents_expiry', 'web_tree_image'],
    'category': 'hr',
    'summary': 'oh_employee_documents_expiry Extensions',

    'data': [
        "views/eq_hr_employee_document.xml",
        "views/eq_functions.xml",
    ],
    'installable': True,
    'auto_install': False,
}
