# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Equitania Einkauf Sektion",
    'license': 'AGPL-3',
    'version': '1.0.0',
    'category': 'purchase',
    'description': """Equitania Einkauf Sektion""",
    'author': 'Equitania Software GmbH',
    'summary': 'Purchase Extension',
    'website': 'www.myodoo.de',
    "depends": ['base', 'purchase','eq_report_pattern'],
    'data': [ 'views/purchase_order.xml',
              'reports/report_purchaseorder.xml'
             ],
    "installable": True
}
