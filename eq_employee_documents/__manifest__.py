# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Equitania Mitarbeiterdokumente',
    'license': 'AGPL-3',
    'version': '1.0.7',
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
