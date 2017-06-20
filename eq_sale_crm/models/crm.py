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

from openerp import models, fields, api, _


class eq_crm_lead(models.Model):
    _inherit = 'crm.lead'

    # _order = "date_action,priority desc,id desc"

    def compute_quot_crm_count(self):
        sale_order_obj = self.env['sale.order']
        for crm in self:
            record = sale_order_obj.search([('partner_id', '=', crm.partner_id.id)])
            crm_quot_count = len(record)
            crm.total_quot_crm = str(crm_quot_count)

    total_quot_crm = fields.Char(compute='compute_quot_crm_count', string="Quotations")