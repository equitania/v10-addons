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
    'name': 'Equitania Dokumenten Bausteine',
    'license': 'AGPL-3',
    'version': '1.0.25',
    'description': """
        Improves the odoo document templating, overwrites head- and foot-texttemplates
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base', 'base_setup', 'website_quote', 'stock', 'sales_team', 'eq_sale', 'eq_purchase', 'eq_account'],
    'category' : 'Reports',
    'summary': '',
    'data': [
            'security/ir.model.access.csv',
            'views/document_template_view.xml',
            'views/sale_view.xml',
            'views/purchase_view.xml',
            'views/stock_picking_view.xml',
            'views/account_invoice_view.xml',
            'views/res_partner_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
