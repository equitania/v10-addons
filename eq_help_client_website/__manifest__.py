# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'MyOdoo Help Client for Frontend',
    'summary': """
        MyOdoo Help Client for Frontend will Create Buttons for Models which will request Help form the Help Server
        """,
    'version': '1.0.1',
    'author': "Callino, improved by Equitania Software GmbH",
    'maintainer': 'Callino, improved by Equitania Software GmbH',
    'website': 'https://equitania.atlassian.net/wiki/spaces/MH/overview',
    'license': 'AGPL-3',
    'category': 'Documentation',
    'depends': [
        'website', 'website_sale', 'eq_help_client'
    ],
    'data': [
        'views/assets.xml',
        'views/eq_help_client_frontend.xml',
    ],
    'qweb': [
    ],
    'installable': True,
    'auto_install': False
}
