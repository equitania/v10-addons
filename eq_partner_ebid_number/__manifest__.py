# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Equitania EBID Integration Unternehmensverzeichnis.org',
    'version': '1.0.8',
    'description': """
        Equitania Software GmbH
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup', 'sales_team'],
    'category' : 'General Improvements',
    #What it Improves e.g Sale, Purchase, Accounting
    'summary': '',
    'data': [
        'security/ir.model.access.csv',
        'views/partner_view.xml',
        'views/eq_ebid_config_view.xml',
        'views/eq_ebid_check_job.xml',
        'views/eq_ebid_protocol_view.xml',
        
    ],
    #Demodata
    'demo': [],
    #Activates css for the view
    #'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
