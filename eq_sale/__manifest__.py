# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Equitania Sale",
    'license': 'AGPL-3',
    'version': '1.0.100',
    'category': 'sale',
    'description': """Extensions for sale""",
    'author': 'Equitania Software GmbH',
    'summary': 'Sale Extension',
    'website': 'www.myodoo.de',
    "depends" : ['base', 'base_setup', 'sale', 'product', 'sales_team', 'sale_stock', 'delivery', 'eq_res_partner', 'eq_base_report','website_quote', 'sale_order_line_sequence'],
    'data': [
            'security/equitania_security.xml',
            'security/ir.model.access.csv',
            'data/decimal_precision.xml',
            'data/ir_values_defaults.xml',
            'views/report_sale_order.xml',
            'views/product_view.xml',
            'views/res_partner_view.xml',
            'views/sale_views.xml',
            'views/sale_layout_category_view.xml',
             ],
    "active": False,
    "installable": True
}
