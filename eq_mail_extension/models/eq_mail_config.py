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

from odoo import fields, models, api
from odoo.tools.translate import _

class eq_mail_config_settings(models.TransientModel):
    _name = 'eq_mail_config.settings'
    _inherit = 'res.config.settings'    

    @api.model
    def set_default_mail_server(self):
        ir_values = self.env['ir.values']
        config = self.browse( self.ids)
        ir_values.set_default('mail.mail', 'mail_server_id', config.mail_server_id and config.mail_server_id.id or False)
        ir_values.set_default('mail.mail', 'mail_server_address', config.mail_server_address or False)

    @api.model
    def get_default_mail_server(self, context=None):
        receivable = self.env['ir.values'].get_default('mail.mail','mail_server_id')

        existing_ir_mail_server = self.env['ir.mail_server'].search([('id','=',receivable)])

        if len(existing_ir_mail_server) > 0:
            address = self.env['ir.mail_server'].browse(receivable)
            receivable = existing_ir_mail_server
        else:
            address = False
            receivable = False
        return {
                #'mail_server_id': receivable,
                #'mail_server_address': address.smtp_user,
                'mail_server_id':existing_ir_mail_server.id if receivable else "",
                'mail_server_address':address.smtp_user if address else "",
                }

    mail_server_id = fields.Many2one('ir.mail_server', 'Default Mail Server',
                                        help="""The outgoing mail server that the system should user for sending e-mails.""")
    mail_server_address =  fields.Char('Default Mails Server Address')

    
    @api.model
    def on_change_mail_server(self, mail_server_id):
        address = self.env['ir.mail_server'].browse(mail_server_id)
        
        values = {
                'mail_server_address': address.smtp_user,
                }
        
        return {'value': values}