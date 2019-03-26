# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Equitania E-Mail-Erweiterung",
    'version': '1.0.48',
    'license': 'AGPL-3',
    'category': 'Mail',
    'description': """Using different smptp settings for user's outgoing emails
    Adds an default mail server for sending System E-Mails 
    and Users without a configured outgoing mail server""",
    'author': 'Equitania Software GmbH',
    'summary': 'E-Mail Extension',
    'website': 'www.myodoo.de',
    "depends" : ['base', 'mail', 'base_setup', 'fetchmail'],
    'data': [
        "security/ir.model.access.csv",
        "data/email_template_function.xml",
        #"data/mail_template_data.xml",
        "views/eq_mail_extension_view.xml",
        "views/eq_mail_config_view.xml",
        "views/eq_base_config_settings_view.xml",
        "views/eq_email_template_view.xml",
        #"wizard/eq_mail_compose_message_view.xml",
    ],
    "active": False,
    "installable": True
}
