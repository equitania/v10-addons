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
            account_line_objs = self.env['account.analytic.line'].search([('project_id','=',project.id),('move_id','=',False),('invoice_id','!=',False)])

            for account_line_obj in account_line_objs:
                proceed = account_line_obj.product_id.standard_price * account_line_obj.eq_time_invoice
                total_proceed = total_proceed + proceed
            project.eq_project_proceeds = total_proceed


    stage_id = fields.Many2one('project.task.type', group_expand='_read_group_stage_ids')
    contract_count = fields.Integer(compute='_compute_contract_count', string='Project Count')
    eq_project_proceeds = fields.Float(compute='_compute_proceeds', string='Product Proceeds')

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
        account_analytic_lines = self.env['account.analytic.line'].search([('project_id','=',self.id),('move_id','=',False),('invoice_id','!=',False)])
        result = {
            "type": "ir.actions.act_window",
            "res_model": "account.analytic.line",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [["id", "in", account_analytic_lines.ids]],
            "context": {"create": False},
            "name": _("Timesheet"),
        }
        return result






