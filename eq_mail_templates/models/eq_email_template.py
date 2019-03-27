# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http, api, fields, models
import logging

_logger = logging.getLogger(__name__)


class email_template(models.Model):
    _inherit = 'mail.template'

    eq_email_template_version = fields.Integer(string="Version Number")

class eq_install_func(models.Model):
    """
        Hilfsklasse mit Funktionen, die wir bei der Installation des Modules ausführen wollen..z.B. Defalt Email-Vorlagen löschen
    """
    _name = "eq_delete_mail_func"

    def _eq_delete_default_templates_rest_pw(self):
        """
            Wir löschen hier Default E-Mail Vorlage für die Reset PW, die wir durch unsere Version ersetzen
        """
        reset_pw_email_templates = self.env['mail.template'].sudo().search([('name', '=', 'Reset Password')])
        for reset_pw_record in reset_pw_email_templates:
            reset_pw_record.unlink()

    def _eq_delete_default_templates_invoice(self):
        """
        Wir löschen hier Default E-Mail Vorlage für die Invoice, die wir durch unsere Version ersetzen
        """
        _logger.info("** Deleting default email templates **")

        delete_default_template = self.env['mail.template'].sudo().search([('name', '=', 'Invoice - Send by Email')])
        delete_template = self.env['mail.template'].sudo().search([('name', '=', 'Invoice -  Send by E-Mail')])
        delete_template_3 = self.env['mail.template'].sudo().search([('eq_email_template_version', '=', 0),('name', '=', 'Rechnung')])
        delete_template_4 = self.env['mail.template'].sudo().search([('eq_email_template_version', '=', 0),('name', '=', 'Notification Email')])

        for delf_default_record in delete_default_template:
            delf_default_record.unlink()
        for del_record in delete_template:
            del_record.unlink()
        for del_3_record in delete_template_3:
            del_3_record.unlink()
        for del_4_record in delete_template_4:
            del_4_record.unlink()

    def _eq_delete_default_templates_purchase(self):
        """
        Wir löschen hier Default E-Mail Vorlage für die Purchase, die wir durch unsere Version ersetzen
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


    def _eq_delete_default_templates_sale(self):
        """
        Wir löschen hier Default E-Mail Vorlage für die Sale, die wir durch unsere Version ersetzen
        """
        _logger.info("** Deleting default email templates **")
        email_templates = self.env['mail.template'].sudo().search([('name','=','Sales Order - Send by Email')])
        for record in email_templates:
            record.unlink()

        email_templates = self.env['mail.template'].sudo().search([('eq_email_template_version', '=', False),('name', '=', 'Notification Email')])
        for record in email_templates:
            record.unlink()

    ################################### Version 2

    def _eq_delete_default_templates_contract(self):
        """
        Wir löschen hier Default E-Mail Vorlage für die Sale, die wir durch unsere Version ersetzen
        """
        _logger.info("** Deleting default email templates **")
        email_templates = self.env['mail.template'].sudo().search([('eq_email_template_version', '=', False),('name','=','Email Contract Template')])
        for record in email_templates:
            record.unlink()

    def _eq_delete_default_templates_calendar(self):
        """
        Wir löschen hier Default E-Mail Vorlage für die Sale, die wir durch unsere Version ersetzen
        """
        _logger.info("** Deleting default email templates **")
        # email_templates = self.env['mail.template'].sudo().search([('eq_email_template_version', '=', False),('name','=','Calendar: Date updated')])
        # for record in email_templates:
        #     record.unlink()
        email_templates_2 = self.env['mail.template'].sudo().search([('eq_email_template_version', '=', False),('name', '=', 'Calendar: Meeting Invitation')])
        for record in email_templates_2:
            record.unlink()
        email_templates_3 = self.env['mail.template'].sudo().search([('eq_email_template_version', '=', False),('name', '=', 'Calendar: Reminder')])
        for record in email_templates_3:
            record.unlink()

    def _eq_delete_default_templates_auth(self):
        """
        Wir löschen hier Default E-Mail Vorlage für die Sale, die wir durch unsere Version ersetzen
        """
        _logger.info("** Deleting default email templates **")
        email_templates = self.env['mail.template'].sudo().search([('eq_email_template_version', '=', False),('name','=','Auth Signup: Odoo Connection')])
        for record in email_templates:
            record.unlink()

    def _eq_delete_default_templates_crm(self):
        """
        Wir löschen hier Default E-Mail Vorlage für die Sale, die wir durch unsere Version ersetzen
        """
        _logger.info("** Deleting default email templates **")
        email_templates = self.env['mail.template'].sudo().search([('eq_email_template_version', '=', False),('name','=','Lead: Reminder')])
        for record in email_templates:
            record.unlink()
