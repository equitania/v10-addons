# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Equitania Verkauf & Lager",
    'license': 'AGPL-3',
    'version': '1.0.18',
    'category': 'sale_stock',
    'description': """ Improved view for order items""",
    'author': 'Equitania Software GmbH',
    'summary': ' Erweiterung Verkauf / Lager',
    'website': 'www.myodoo.de',
    "depends" : ['base', 'base_setup', 'eq_stock', 'sales_team', 'sale_stock', 'eq_sale', 'eq_product'],
    'data': [
            'security/ir.model.access.csv',
            'views/eq_open_sale_order_line_view.xml',
            'views/eq_stock_picking_view.xml',
            'views/eq_sql_function_on_update.xml',
            'views/eq_stock_pack_operation_view.xml',
             ],
    "active": False,
    "installable": True
}
