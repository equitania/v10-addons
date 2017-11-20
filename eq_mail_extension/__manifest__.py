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
    'name': "Equitania E-Mail-Erweiterung",
    'version': '1.0.31',
    'license': 'AGPL-3',
    'category': 'Mail',
    'description': """Using different smptp settings for user's outgoing emails
    Adds an default mail server for sending System E-Mails and Users without a configured outgoing mail server""",
    'author': 'Equitania Software GmbH',
    'summary': 'E-Mail Extension',
    'website': 'www.myodoo.de',
    "depends" : ['base', 'mail', 'base_setup', 'fetchmail'],
    'data': [
             "security/ir.model.access.csv",
             "data/email_template_function.xml",
             "data/mail_template_data.xml",
             "views/eq_mail_extension_view.xml",
             "views/eq_mail_config_view.xml",
             "views/eq_base_config_settings_view.xml",
             "views/eq_email_template_view.xml",
             ],
    "active": False,
    "installable": True
}
