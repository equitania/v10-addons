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
    'version': '1.0.62',
    'category': 'sale',
    'description': """Extensions for sale""",
    'author': 'Equitania Software GmbH',
    'summary': 'Sale Extension',
    'website': 'www.myodoo.de',
    "depends" : ['base', 'base_setup', 'sale', 'product', 'sales_team', 'sale_stock', 'delivery', 'eq_res_partner', 'eq_base_report','website_quote'],
    'data': [
            'security/equitania_security.xml',
            'security/ir.model.access.csv',
            'data/template_sale_order_notification.xml',
            'data/email_template_function.xml',
            'data/decimal_precision.xml',
            'data/ir_values_defaults.xml',
            'data/sales_order_send_by_email.xml',
            'views/report_sale_order.xml',
            'views/product_view.xml',
            'views/res_partner_view.xml',
            'views/sale_views.xml',
            'views/sale_layout_category_view.xml',
             ],
    "active": False,
    "installable": True
}
