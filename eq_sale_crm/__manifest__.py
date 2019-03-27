# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Equitania Verkauf- & CRM Optimierungen',
    'license': 'AGPL-3',
    'version': '1.0.4',
    'description': """
        Extensions for sale_crm
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    #'depends': ['base_setup', 'base', 'sale', 'crm', 'sale_crm'],      # Sody: 09.08.2017 - original vor der Erweiterung der Docu
    'depends': ['base_setup', 'base' , 'sale_crm'],
    'category' : 'CRM Sale',
    'summary': 'Sale_crm extensions',

    'data': [
        "views/crm_view.xml",
    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
