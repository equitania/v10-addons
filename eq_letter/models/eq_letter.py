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

class eq_letter(models.Model):
    _name = 'eq_letter'
    _rec_name = 'eq_letter_subject'

    eq_text = fields.Html('Text', required=True)

    def get_current_user(self):
        obj = self.env['res.users'].search([('id','=',self._uid)])
        return obj.partner_id

    eq_letter_from = fields.Many2one('res.partner', string='From', default=get_current_user, required=True)
    eq_letter_subject = fields.Char('Subject', required=False)
    eq_letter_to = fields.Many2one('res.partner', string="To", required=True)


