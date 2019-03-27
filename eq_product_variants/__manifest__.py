# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Equitania Produktvarianten',
    'license': 'AGPL-3',
    'version': '1.0.2',
    'description': """
        Remove SQL Contraint from product.template (eq.product)
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup', 'eq_product'],
    'category' : 'General Improvements',
    'summary': 'Remove SQL Contraint from product.template (eq.product)',

    'data': [
        #"security/ir.model.access.csv"
        "views/eq_product_supplier_view.xml",
    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
