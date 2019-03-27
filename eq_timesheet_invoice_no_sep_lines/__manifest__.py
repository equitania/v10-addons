# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Equitania Timesheet Invoice",
    'description': "Avoid for every account.analytic.line an own account.invoice.line",
    'version': '10.0.0.1.6',
    'author': 'Equitania Software GmbH',
    'license': 'AGPL-3',
    'category': 'Custom',
    'website': 'https://www.myodoo.de',
    'depends': ['sale', 'hr_timesheet', 'analytic', 'contract','project','timesheet_invoice'],
    'data': [
        ],
    'installable': True,
}
