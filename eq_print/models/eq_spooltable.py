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

from odoo import models, fields, api, _

class eq_spooltable(models.Model):
    _name = 'eq.spooltable'
    _order = 'id desc'
    
    def _get_default_printer(self):
        user = self.env['res.users'].browse(self._uid)
        if user.eq_default_printer_id:
            return user.eq_default_printer_id.id
        else:
            return False
    
    def _get_default_user(self):
        if self._uid:
            return self._uid
        else:
            return False
    
    eq_printer_id = fields.Many2one(string="Printer", comodel_name="eq.printer", default=_get_default_printer, required=True)
    eq_document_name = fields.Char(string="Document Name")
    eq_user_id = fields.Many2one(string="User", comodel_name="res.users", default=_get_default_user, required=True)
    eq_copies = fields.Integer(string="Copies", default=1, required=True)
    eq_file = fields.Binary(string="PDF File", required=True)
    state = fields.Selection(string="State", selection=[("open", "Open"), ("print", "Printing"), ("done", "Done"), ("cancel", "Canceled")], default="open")
    create_date = fields.Datetime(string="Created on")
    
    @api.multi
    def do_cancel(self):
        self.write({'state': 'cancel'})
        return True
    
    @api.multi
    def do_reopen(self):
        self.write({'state': 'open'})
        return True
    
    @api.multi
    def do_done(self):
        self.write({'state': 'done'})
        return True
    
    @api.multi
    def do_print(self):
        self.write({'state': 'print'})
        return True
    
    @api.model
    def get_spooltable_for_user(self):
        res = self.search_read([('eq_user_id', '=', self._uid), ('state', '=', 'open')], ['id'])
        return res
    
    @api.one
    def get_data(self):
        vals = {
                'id': self.id,
                'printer': self.eq_printer_id.eq_name,
                'copies': self.eq_copies,
                'file': self.eq_file,
                'document_name': self.eq_document_name,
                'state': self.state,
                }
        return vals