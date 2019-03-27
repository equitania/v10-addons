# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Equitania Translation Modul",
    'license': 'AGPL-3',
    'version': '1.0.2',
    'category': 'sales',
    'description': """ Extension for the translation file""",
    'author': 'Equitania Software GmbH',
    'summary': ' Change the standard translations',
    'website': 'www.myodoo.de',
    "depends" : ['base',  'sale_stock'],
    'data': [

            'views/eq_sale_stock_translation.xml',
             ],
    "active": False,
    "installable": True
}