# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Equitania Report Erweiterung für OCA Modul "product_customer_code"',
    'license': 'AGPL-3',
    'version': '1.0.0',
    'description': """
        Equitania Report Erweiterung für OCA Modul "product_customer_code"
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup','eq_sale','product_customer_code','eq_account'],
    'category' : 'General Improvements',
    'summary': 'Equitania Report Erweiterung für OCA Modul "product_customer_code"',

    'data': [
        #"security/ir.model.access.csv"
        "views/eq_report_sale_order.xml",
        "views/eq_report_stock_picking.xml",
        "views/eq_report_account_invoice.xml",

    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
