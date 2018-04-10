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
    'version': '1.0.1',
    'description': """
        Mail Templates
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup','mail','eq_account','eq_sale','eq_purchase'],
    'category' : 'General Improvements',
    'summary': 'Mail Templates',

    'data': [
        "security/ir.model.access.csv",
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
