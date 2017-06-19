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


class eq_crm_lead(models.Model):
    _inherit = 'crm.lead'

    firstname = fields.Char('Firstname')
    lastname = fields.Char('Lastname')
    category_ids = fields.Many2many('res.partner.category', string='Tags')
    website = fields.Char('Website')
    birthdate = fields.Date('Birthday')
    eq_citypart = fields.Char('District')
    eq_house_no = fields.Char('House Number')

    # @api.onchange('state_id')
    # def _onchange_state(self):
    #     super(eq_crm_lead, self)._onchange_state()

