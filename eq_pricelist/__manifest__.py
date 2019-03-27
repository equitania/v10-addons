# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Equitania Preislisten Optimierungen",
    'license': 'AGPL-3',
    'version': '1.0.7',
    'category': 'pricelist',
    'description': """ Extension for pricelist-positions """,
    'author': 'Equitania Software GmbH',
    'summary': 'Pricelist Extension',
    'website': 'www.myodoo.de',
    "depends" : ['base', 'base_setup', 'product', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/eq_pricelist_view.xml',
        ],
    "active": False,
    "installable": True
}
