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
    'name': "Equitania Translation Modul",
    'license': 'AGPL-3',
    'version': '1.0.0',
    'category': 'sales',
    'description': """ Extension for the translation file""",
    'author': 'Equitania Software GmbH',
    'summary': ' Change the standard translations',
    'website': 'www.myodoo.de',
    "depends" : ['base',  'sale_stock'],
    'data': [

            'views/eq_sale_stock_translation.xml',
             ],
    "active": False,
    "installable": True
}