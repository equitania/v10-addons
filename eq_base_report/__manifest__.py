# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Equitania Ausdrucke Basis',
    'license': 'AGPL-3',
    'version': '1.0.41',
    'description': """
        Allgemeine Anpassungen für die Equitania Reports
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup','eq_base'],
    'category' : 'Report',
    'summary': 'Reports',

    'data': [
        'views/footer.xml',
        'views/header.xml',
        'views/paper_format.xml',
        'views/report_external_layout.xml',
        'views/report_internal_layout.xml',
        'views/report_style.xml',
        'eq_res_config_view.xml'

    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
