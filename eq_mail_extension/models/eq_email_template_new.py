# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)

class MailTemplate(models.Model):
    """Templates for sending email"""
    _inherit = "mail.template"

    name = fields.Char('Name', translate=True)


class EqInstallFunc(models.Model):
    """
        Hilfsklasse mit Funktionen, die wir bei der Installation des Modules ausführen wollen..z.B. Defalt Email-Vorlagen löschen
    """
    _name = "eq_install_func"

    def _eq_delete_default_templates(self):
        """
        Wir löschen hier Default E-Mail Vorlage für die Bestellbestätigung, die wir durch unsere Version ersetzen
        """
        _logger.info("** Deleting default email templates **")
        email_templates = self.env['mail.template'].sudo().search([('eq_email_template_version', '=', False), ('name', '=', 'Invoice Notification Email')])
        for record in email_templates:
            record.unlink()

        email_templates = self.env['mail.template'].sudo().search([('eq_email_template_version', '=', False), ('name', '=', 'Sale Order Notification Email')])
        for record in email_templates:
            record.unlink()
