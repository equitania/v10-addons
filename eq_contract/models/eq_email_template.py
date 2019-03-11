# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import http, api, fields, models
import logging

_logger = logging.getLogger(__name__)


class eq_install_func(models.Model):
    """
        Hilfsklasse mit Funktionen, die wir bei der Installation des Modules ausführen wollen..z.B. Defalt Email-Vorlagen löschen
    """
    _name = "eq_delete_mail_func"

    def _eq_delete_default_templates_contract(self):
        """
        Wir löschen hier Default E-Mail Vorlage für die Sale, die wir durch unsere Version ersetzen
        """
        _logger.info("** Deleting default email templates **")
        email_templates = self.env['mail.template'].sudo().search([('eq_email_template_version', '=', False),('name','=','Email Contract Template')])
        for record in email_templates:
            record.unlink()
