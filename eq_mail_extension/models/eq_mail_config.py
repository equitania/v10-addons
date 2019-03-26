# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api

class EqMailConfigSettings(models.TransientModel):
    """EqMailConfigSettings class inherited from ResConfigSettings class"""
    _name = 'eq_mail_config.settings'
    _inherit = 'res.config.settings'

    @api.model
    def set_default_mail_server(self):
        ir_values = self.env['ir.values']
        config = self.browse(self.ids)
        ir_values.set_default('mail.mail', 'mail_server_id', config.mail_server_id and config.mail_server_id.id or False)
        ir_values.set_default('mail.mail', 'mail_server_address', config.mail_server_address or False)

    @api.model
    def get_default_mail_server(self, context=None):
        receivable = self.env['ir.values'].get_default('mail.mail', 'mail_server_id')
        existing_ir_mail_server = self.env['ir.mail_server'].search([('id', '=', receivable)])

        if existing_ir_mail_server:
            address = self.env['ir.mail_server'].browse(receivable)
            receivable = existing_ir_mail_server[0]
        else:
            address = False
            receivable = False
        return {
            #'mail_server_id': receivable,
            #'mail_server_address': address.smtp_user,
            'mail_server_id':existing_ir_mail_server.id if receivable else "",
            'mail_server_address':address.smtp_user if address else "",
            }

    mail_server_id = fields.Many2one(
        'ir.mail_server',
        'Default Mail Server',
        help="The outgoing mail server that the system should user for sending e-mails.")
    mail_server_address = fields.Char('Default Mails Server Address')


    @api.model
    def on_change_mail_server(self, mail_server_id):
        address = self.env['ir.mail_server'].browse(mail_server_id)

        values = {
            'mail_server_address': address.smtp_user,
            }

        return {'value': values}
