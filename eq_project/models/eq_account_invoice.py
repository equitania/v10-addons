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
from datetime import datetime, timedelta

class eq_account_invoice_project(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_invoice_cancel(self):
        res = super(eq_account_invoice_project, self).action_invoice_cancel()
        del_line_links = self.env['account.analytic.line'].search([('invoice_id', '=', self.id)])
        for del_line_link in del_line_links:
            del_line_link.write({'invoice_id': False, 'eq_storno_flag': 'True'})
        return res

class eq_projectAccountInvoiceRefund(models.TransientModel):
    """Refunds invoice"""

    _inherit = "account.invoice.refund"

    @api.multi
    def invoice_refund(self):
        res = super(eq_projectAccountInvoiceRefund, self).invoice_refund()
        context = self._context
        if 'active_id' in context:
            active_id = context['active_id']
            del_line_links = self.env['account.analytic.line'].search([('invoice_id', '=', active_id)])
            for del_line_link in del_line_links:
                del_line_link.write({'invoice_id': False, 'eq_storno_flag': 'True'})
        elif 'active_ids' in context:
            active_ids = context['active_ids']
            for active_id in active_ids:
                del_line_links = self.env['account.analytic.line'].search([('invoice_id', '=', active_id)])
                for del_line_link in del_line_links:
                    del_line_link.write({'invoice_id': False, 'eq_storno_flag': 'True'})
        return res