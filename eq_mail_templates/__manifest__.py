# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo Addon, Open Source Management Solution
#    Copyright (C) 2014-now Equitania Software GmbH(<http://www.equitania.de>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Equitania Mail Templates',
    'license': 'AGPL-3',
    'version': '1.0.10',
    'description': """
        Verbesserte Mail Templates für Sales / Purchase / Account Invoice
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup','mail','eq_account','eq_sale','eq_purchase','calendar','crm'],
    'category': 'General Improvements',
    'summary': 'Mail Templates',

    'data': [
        "security/ir.model.access.csv",
        "data/mail_template_data.xml",
        #"data/calendar_date_updated.xml",        #not in use, because: the super-write method tries to load the old template which would be overwritten by our template
        "data/calendar_meeting_invitation.xml",
        "data/calendar_reminder.xml",
        "data/crm_lead_data.xml",
        "data/auth_signup.xml",
        "data/email_template_function_auth_signup.xml",
        "data/email_template_function_calendar.xml",
        "data/email_template_function_crm.xml",
        "data/email_template_function_invoice.xml",
        "data/email_template_function_purchase.xml",
        "data/email_template_function_reset_pw.xml",
        "data/email_template_function_sale.xml",
        "data/invoice_send_by_email.xml",
        "data/purchase_order_send_by_email.xml",
        "data/reset_password.xml",
        "data/rfq_send_by_email.xml",
        "data/sales_order_send_by_email.xml",
        "data/template_account_invoice_notification.xml",
        "data/template_sale_order_notification.xml",

    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
