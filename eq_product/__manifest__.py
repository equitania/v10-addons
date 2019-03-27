# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Equitania Produkt Optimierungen",
    'license': 'AGPL-3',
    'version': '1.0.27',
    'category': 'product',
    'description': """Extensions for product""",
    'author': 'Equitania Software GmbH',
    'summary': 'Product Extension',
    'website': 'www.myodoo.de',
    "depends" : ['base', 'base_setup', 'product', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
        'views/product_config_view.xml',
        'views/report_label_product_product_templates.xml',
        'data/ir_sequence_data.xml',
        ],
    "active": False,
    "installable": True
}
