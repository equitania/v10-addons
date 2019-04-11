# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'MyOdoo Help Client',
    'summary': """
        MyOdoo Help Client will Create Buttons for Models which will request Help form the Help Server
        """,
    'version': '1.0.10',
    'author': "Callino, improved by Equitania Software GmbH",
    'maintainer': 'Callino, improved by Equitania Software GmbH',
    'website': 'https://equitania.atlassian.net/wiki/spaces/MH/overview',
    'license': 'AGPL-3',
    'category': 'Documentation',
    'depends': [
        #'website',
    ],
    'data': [
        'data/parameters.xml',
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/eq_help_client.xml',
    ],
    'installable': True,
    'auto_install': False
}
