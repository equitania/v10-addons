# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Equitania CRM Optimierungen",
    'license': 'AGPL-3',
    'version': '1.0.5',
    'category': 'crm',
    'description': """Extensions for crm leads""",
    'author': 'Equitania Software GmbH',
    'summary': 'Lead Extension',
    'website': 'www.myodoo.de',
    "depends" : ['base', 'base_setup', 'crm'],
    'data': [
            'views/crm_view.xml',
            'data/eq_crm_stage_data.xml'
             ],
    "active": False,
    "installable": True
}
