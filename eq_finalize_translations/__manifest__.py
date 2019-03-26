# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

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