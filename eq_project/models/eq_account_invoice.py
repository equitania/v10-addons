# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

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

class EqAccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.multi
    def unlink(self):
        """
        Unlink function for removing the link to the invoice in account.analytic.line if  linked account.invoice.line is removed
        :return: res
        """
        # eq_invoice_line_id is defined in timesheet_invoice module
        account_analytic_lines = self.env['account.analytic.line'].search([('eq_invoice_line_id','in',self.ids)])
        res = super(EqAccountInvoiceLine, self).unlink()
        if res:
            if account_analytic_lines:
                for account_analytic_line in account_analytic_lines:
                    account_analytic_line.write({'invoice_id': False, 'eq_storno_flag': 'True'})

        return res