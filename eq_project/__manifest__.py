# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Equitania Projekt",
    'license': 'AGPL-3',
    'version': '1.0.69',
    'category': 'project',
    'description': """Extensions for project""",
    'author': 'Equitania Software GmbH',
    'summary': 'Project Extension',
    'website': 'www.myodoo.de',
    "depends" : ['base','project','project_issue','hr_timesheet_activity_begin_end','hr_timesheet_sheet', 'analytic','project_recalculate',
                 'timesheet_invoice','project_description','sale_timesheet',
                 'project_task_category','project_task_code','project_task_report','project_timeline','project_parent','project_issue_sheet','eq_account','hr_timesheet_task'],  #no dependencies for stage was always in Project/Data/project_data.xml declared
    'data': [
            'data/ir_sequence_data.xml',
            'views/eq_project_extension_view.xml',
            'views/eq_issues_extension.xml',
            'views/eq_project_task_view.xml',
            'views/eq_extension_project_task_type.xml',
            'views/eq_project_settings.xml',
            'views/report_account_extension.xml',
            'views/report_timesheet_extension.xml',
            'views/eq_report_timesheet_extension_invoice.xml',
            'views/eq_hr_timesheet_assets.xml',
            'views/project_task_report_extension.xml',
            'views/project_task_chatter_report_extension.xml',
             ],
    "active": False,
    "installable": True
}
