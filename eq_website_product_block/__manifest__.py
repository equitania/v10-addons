# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Equitania Website Product Block',
    'license': 'AGPL-3',
    'version': '1.0.1',
    'description': "Fügt einen Bereich für Produktbeschreibungen in der Produktdetailansicht hinzu",
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup', 'website_sale'],
    'category' : 'website sale',
    'summary': 'Fügt einen Bereich für Produktbeschreibungen in der Produktdetailansicht hinzu',

    'data': [
        "templates.xml",
    ],
    'demo': [],
    'css': ['base.css'],
    'active': False,
    'installable': True,
    'auto_install': False,
}
