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

from odoo import http, api, fields, models
import logging

_logger = logging.getLogger(__name__)

class eq_install_func(models.Model):
    """
        Hilfsklasse mit Funktionen, die wir bei der Installation des Modules ausführen wollen..z.B. Defalt Email-Vorlagen löschen
    """
    _name = "eq_install_func"

    def _eq_delete_default_templates(self):
        """
        Wir löschen hier Default E-Mail Vorlage für die Bestellbestätigung, die wir durch unsere Version ersetzen
        """
        _logger.info("** Deleting default email templates **")
        email_templates = self.env['mail.template'].sudo().search([('eq_email_template_version','=',False),('name','=','Purchase Order - Send by Email')])
        for record in email_templates:
            record.unlink()
        email_templates = self.env['mail.template'].sudo().search([('eq_email_template_version', '=', False), ('name', '=', 'RFQ - Send by Email')])
        for record in email_templates:
            record.unlink()

        po_email_templates = self.env['mail.template'].sudo().search([('name', '=', 'Purchase Order - Send by Email')])
        for po_record in po_email_templates:
            po_record.unlink()
        rfq_email_templates = self.env['mail.template'].sudo().search([('name', '=', 'RFQ - Send by Email')])
        for rfq_record in rfq_email_templates:
            rfq_record.unlink()