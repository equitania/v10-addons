# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Equitania Sale VAT Check",
    'license': 'AGPL-3',
    'version': '1.0.2',
    'category': 'sale',
    'description': """Extensions for VAT Check""",
    'author': 'Equitania Software GmbH',
    'summary': 'Extensions for VAT Check',
    'website': 'www.myodoo.de',
    "depends" : ['base', 'sale','base_vat','account'],
    'data': ['views/account_fiscal_position.xml'],
    "installable": True
}
