# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Equitania Einkauf Optimierungen",
    'license': 'AGPL-3',
    'version': '1.0.45',
    'category': 'purchase',
    'description': """Extensions for purchase""",
    'author': 'Equitania Software GmbH',
    'summary': 'Purchase Extension',
    'website': 'www.myodoo.de',
    "depends": ['base', 'base_setup', 'purchase', 'eq_res_partner', 'eq_base_report'],
    'data': [
        'data/decimal_precision.xml',
        'views/purchase_view.xml',
        'views/report_purchase_order.xml',
        'views/report_purchase_quotation.xml',
        'views/eq_res_partner_view.xml',
             ],
    "active": False,
    "installable": True
}
