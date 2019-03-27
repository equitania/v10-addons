# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Equitania Setting Unbrand",
    'license': 'AGPL-3',
    'version': '1.0.7',
    'category': 'Settings',
    'description': """ Entfernt die Odoo Brandings und ersetzt
    Sie durch MyOdoo Links und Wiki-links
    """,
    'author': 'Equitania Software GmbH',
    'summary': 'Unbrand Extension',
    'website': 'www.myodoo.de',
    'depends' : ['web_settings_dashboard', 'base_setup', 'report'],
    'data': [
        #'security/ir.model.access.csv',
        #'views/style_extension.xml',      #wird derzeit nicht benötigt und deshalb deaktiviert
        'views/report_settings.xml',
        ],
    'qweb': [
        'static/src/xml/dashboard_extension.xml',
        ],

    "active": False,
    "installable": True
}
