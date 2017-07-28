# -*- coding: utf-8 -*-
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Equitania Cookie Notiz Erweiterung',
    'summary': 'Optische und sprachliche Verbesserungen an der Cookie Notiz',
    'version': '1.0.1',
    'category': 'Website',
    'author': "Equitania Software GmbH",

    'website': 'www.myodoo.de / www.equitania.de',
    'license': 'AGPL-3',
    'depends': [
        'website_legal_page','website_cookie_notice',
    ],
    'data': [
        'templates/website.xml',
    ],

    'installable': True,
    'auto_install': False,
}
