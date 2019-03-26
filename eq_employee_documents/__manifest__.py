# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Equitania Mitarbeiterdokumente',
    'license': 'AGPL-3',
    'version': '1.0.6',
    'description': """
        Extensions for module oh_employee_documents_expiry
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup', 'base', 'hr', 'oh_employee_documents_expiry', 'web_tree_image'],
    'category': 'hr',
    'summary': 'oh_employee_documents_expiry Extensions',

    'data': [
        "views/eq_hr_employee_document.xml",
        "views/eq_functions.xml",
    ],
    'installable': True,
    'auto_install': False,
}
