# -*- coding: utf-8 -*-
{
    'name': 'MyOdoo Help Client',
    'summary': """
        MyOdoo Help Client will Create Buttons for Models which will request Help form the Help Server
        """,
    'version': '1.0.3',
    'author': "Callino, improved by Equitania Software GmbH",
    'maintainer': 'Callino, improved by Equitania Software GmbH',
    'website': 'https://equitania.atlassian.net/wiki/spaces/MH/overview',
    'license': 'AGPL-3',
    'category': 'Documentation',
    'depends': [
        'website',
    ],
    'data': [
        'data/parameters.xml',
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/eq_help_client.xml',
    ],
    'installable': True,
}
