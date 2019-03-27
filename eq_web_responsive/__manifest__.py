# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Equitania Responsive Interface',
    'license': 'AGPL-3',
    'version': '1.0.12',
    'description': """
        Anpassung für das Backend Theme web_responsive
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['web_responsive', 'base_setup'],
    'category' : 'backend',
    'summary': 'backend improvement',

    'data': [
        "views/assets.xml"

    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
