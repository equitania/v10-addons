# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Equitania Kontakt Erweiterung",
    'license': 'AGPL-3',
    'version': '1.0.2',
    'category': 'Partner',
    'description': """Extensions for eq_res_partner""",
    'author': 'Equitania Software GmbH',
    'summary': 'Partner Extension',
    'website': 'www.myodoo.de',
    "depends" : ['base', 'eq_res_partner','web_readonly_bypass'],
    'data': [
            "views/eq_res_partner_view.xml",
             ],
    "active": False,
    "installable": True
}
