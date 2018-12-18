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
    'name': "Equitania Separate Stock Picking",
    'license': 'AGPL-3',
    'version': '1.0.2',
    'category': 'sale_stock',
    'description': """Separate stock_picking creation after sale_order confirmation""",
    'author': 'Equitania Software GmbH',
    'summary': 'StockMove Extension',
    'website': 'www.myodoo.de',
    "depends" : ['eq_sale_stock'],
    'data': [ ],
    "active": False,
    "installable": True
}
