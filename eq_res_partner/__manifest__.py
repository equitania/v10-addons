# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Equitania Kontakt Optimierungen",
    'license': 'AGPL-3',
    'version': '1.0.52',
    'category': 'Partner',
    'description': """Extensions for res_partner""",
    'author': 'Equitania Software GmbH',
    'summary': 'Partner Extension',
    'website': 'www.myodoo.de',
    "depends" : ['base', 'base_setup', 'mail','contacts'],
    'data': [
            "views/eq_res_partner_view.xml",
            "views/eq_res_partner_mails.xml",
            "views/eq_res_company_view.xml",
            "views/eq_res_users_view.xml",
            "views/eq_webclient_templates.xml",
             ],
    "active": False,
    "installable": True
}
