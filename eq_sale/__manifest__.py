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
    'name': "Equitania Sale",
    'license': 'AGPL-3',
    'version': '1.0.4',
    'category': 'product',
    'description': """Extensions for product""",
    'author': 'Equitania Software GmbH',
    'summary': 'Product Extension',
    'website': 'www.myodoo.de',
    "depends" : ['base', 'base_setup', 'sale', 'product', 'sales_team', 'sale_stock', 'eq_res_partner', 'eq_base_report' ],
    'data': [
            'security/ir.model.access.csv',
            'views/report_sale_order.xml',
            'views/reports.xml',
            'product_view.xml',
            'res_partner_view.xml',
            'sale_views.xml',
             ],
    "active": False,
    "installable": True
}
