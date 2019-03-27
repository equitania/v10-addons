# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Equitania Sale Stock Block'
            '',
    'version': '1.5',
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
