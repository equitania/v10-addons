# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Equitania Project Product Type Extension',
    'license': 'AGPL-3',
    'version': '1.0.8',
    'description': """
        Product type Extension for eq_project
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup','eq_project','account'],
    'category' : 'General Improvements',
    'summary': 'Product type Extension for eq_project',

    'data': [
        "security/ir.model.access.csv",
        #"views/eq_product_type_function.xml",
        "views/eq_account_analytic_line_view.xml",
        'views/eq_account_invoice_view.xml',

    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
