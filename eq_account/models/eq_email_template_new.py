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

        delete_default_template = self.env['mail.template'].sudo().search([('name', '=', 'Invoice - Send by Email')])
        delete_template = self.env['mail.template'].sudo().search([('name', '=', 'Invoice -  Send by E-Mail')])
        delete_template_3 = self.env['mail.template'].sudo().search([('eq_email_template_version', '=', 0), ('name', '=', 'Rechnung')])
        for delf_default_record in delete_default_template:
            delf_default_record.unlink()
        for del_record in delete_template:
            del_record.unlink()
        for del_3_record in delete_template_3:
            del_3_record.unlink()
