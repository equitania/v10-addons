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


from odoo import api, fields, models, _

class ProjectProject(models.Model):
    _inherit = 'project.project'

    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['project.task.type'].search([])
        return stage_ids

    def _compute_contract_count(self):
        for project in self:
            if project.analytic_account_id.id:
                project.contract_count = 1
            else:
                project.contract_count = 0

    def _compute_proceeds(self):
        for project in self:
            total_proceed = 0.0
            account_line_objs = self.env['account.analytic.line'].search([('project_id','=',project.id),('move_id','=',False),('eq_invoice_line_id','!=',False)])
            for account_line_obj in account_line_objs:
                if account_line_obj.invoice_id.state != 'draft':
                    proceed = account_line_obj.eq_invoice_line_id.price_subtotal
                    total_proceed = total_proceed + proceed
            refund_account_line_objs = self.env['account.analytic.line'].search([('project_id','=',project.id),('invoice_id','!=',False),('move_id','!=',False)])
            bool_run = False
            for refund_account_line_obj in refund_account_line_objs:
                if refund_account_line_obj.invoice_id.state != 'draft' and refund_account_line_obj.invoice_id.type == 'out_refund':
                    if bool_run == False:
                        for invoice_line in refund_account_line_obj.invoice_id.invoice_line_ids:
                            refund_proceed = invoice_line.price_subtotal
                            total_proceed = total_proceed - refund_proceed
                            bool_run = True
            if total_proceed > 0:
                project.eq_project_proceeds = '+' + str(total_proceed)
            else:
                project.eq_project_proceeds = str(total_proceed)


    stage_id = fields.Many2one('project.task.type', group_expand='_read_group_stage_ids')
    contract_count = fields.Integer(compute='_compute_contract_count', string='Project Count')
    eq_project_proceeds = fields.Char(compute='_compute_proceeds', string='Product Proceeds')

    @api.multi
    def contract_action(self):
        contracts = self.with_context(active_test=False).mapped('analytic_account_id')
        result = {
            "type": "ir.actions.act_window",
            "res_model": "account.analytic.account",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [["id", "in", contracts.ids]],
            "context": {"create": False},
            "name": _("Contracts"),
        }
        if len(contracts) == 1:
            result['views'] = [(False, "form")]
            result['res_id'] = contracts.id
        else:
            result = {'type': 'ir.actions.act_window_close'}
        return result

    @api.multi
    def proceed_action(self):
        account_analytic_lines = self.env['account.analytic.line'].search([('project_id','=',self.id),('move_id','=',False),('eq_invoice_line_id','!=',False)])
        line_list = []
        for account_analytic_line in account_analytic_lines:
            if account_analytic_line.invoice_id.state != 'draft':
                line_list.append(account_analytic_line.id)

        refund_account_line_objs = self.env['account.analytic.line'].search([('project_id', '=', self.id), ('invoice_id', '!=', False), ('move_id', '!=', False)])
        for refund_account_line_obj in refund_account_line_objs:
            if refund_account_line_obj.invoice_id.state != 'draft' and refund_account_line_obj.invoice_id.type == 'out_refund':
                line_list.append(refund_account_line_obj.id)

        result = {
            "type": "ir.actions.act_window",
            "res_model": "account.analytic.line",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [["id", "in", line_list]],
            "context": {"create": False},
            "name": _("Timesheet"),
        }
        return result






