# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Equitania Verträge Erweiterungen',
    'license': 'AGPL-3',
    'version': '1.0.1',
    'description': """
        Equitania Erweiterungen für das Contract Modul der OCA
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['contract'],
    'category' : 'General Improvements',
    'summary': 'Equitania Contract Erweiterungen',

    'data': [
        #"security/ir.model.access.csv"
        "views/eq_contract_view.xml",
        "data/email_template_function_contract.xml",
        "data/contract_template.xml",        #neu

    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
