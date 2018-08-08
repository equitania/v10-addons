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
    'name': 'Equitania Sale Stock Block'
            '',
    'version': '1.3',
    'license': 'AGPL-3',
    'author': 'Equitania Software GmbH',
    'category': 'Custom',
    'website': 'www.myodoo.de',
    'summary': 'Odoo Modifications',
    'description': '''
    Equitania: Blocks stock picking if the related sale order is not payed and is set to block'
''',
    'depends': [
        'base',
        'account',
        'sale_stock',

    ],
    'data': [
        'view/sale.xml',
        'view/account.xml',
        'view/stock_picking.xml',
        'view/stock_picking_type.xml',
    ],
    'js': [],
    'installable': True,
    'application': False,
}
