# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Equitania SQL Exec',
    'version': '1.0.12',
    'license': 'AGPL-3',
    'description': """
        Small SQL helper
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup'],
    'category' : 'Tools',
    'summary': 'EqSqlExec',    
    'data': [         
             'security/ir.model.access.csv',  
             'eq_sql_exec_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
