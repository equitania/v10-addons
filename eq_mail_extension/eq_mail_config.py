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

from openerp.osv import fields, osv
from openerp.tools.translate import _

class eq_mail_config_settings(osv.osv_memory):
    _name = 'eq_mail_config.settings'
    _inherit = 'res.config.settings'    
    
    def set_default_mail_server(self, cr, uid, ids, context=None):
        ir_values = self.pool.get('ir.values')
        config = self.browse(cr, uid, ids[0], context)
        ir_values.set_default(cr, uid, 'mail.mail', 'mail_server_id', config.mail_server_id and config.mail_server_id.id or False)
        ir_values.set_default(cr, uid, 'mail.mail', 'mail_server_address', config.mail_server_address or False)
        
                
    def get_default_mail_server(self, cr, uid, fields, context=None):
        receivable = self.pool.get('ir.values').get_default(cr, uid, 'mail.mail', 'mail_server_id')
        
        #address = self.pool.get('ir.values').get_default(cr, uid, 'mail.mail', 'mail_server_address')
        existing_ir_mail_server = self.pool.get('ir.mail_server').search(cr,uid,[('id','=',receivable)])
        if existing_ir_mail_server != []:
            address = self.pool.get('ir.mail_server').browse(cr, uid,  receivable, context=context)
            receivable = existing_ir_mail_server[0]
        else:
            address = False
            receivable = False
        return {
                #'mail_server_id': receivable,
                #'mail_server_address': address.smtp_user,
                'mail_server_id':existing_ir_mail_server[0] if receivable else "",
                'mail_server_address':address.smtp_user if address else "",
                }

    _columns = {
                'mail_server_id': fields.many2one('ir.mail_server', 'Default Mail Server',
                                                        help="""The outgoing mail server that the system should user for sending e-mails."""),
                'mail_server_address': fields.char('Default Mails Server Address'),
                }
    
    
    def on_change_mail_server(self, cr, uid, ids, mail_server_id, context=None):
        address = self.pool.get('ir.mail_server').browse(cr, uid,  mail_server_id, context=context)
        
        values = {
                'mail_server_address': address.smtp_user,
                }
        
        return {'value': values}