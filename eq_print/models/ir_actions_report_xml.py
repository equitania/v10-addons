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


class eq_ir_actions_report_xml(models.Model):
    _inherit = 'ir.actions.report.xml'

    eq_direct_print = fields.Boolean(string="Remote Print")
    eq_ir_values_id = fields.Many2one(string="Print Menu", comodel_name="ir.values")
    eq_report_wiz_action = fields.Many2one(string="Report Wizard Action", comodel_name="ir.actions.act_window")

    @api.onchange('report_type')
    def _onchange_report_type(self):
        super(eq_ir_actions_report_xml, self)._onchange_report_type()
        self.eq_direct_print = False
        
    @api.multi
    def _get_wiz_action(self):
        self.ensure_one()
        if self.eq_report_wiz_action:
            return self.eq_report_wiz_action.id
        else:
            act_window_obj = self.env['ir.actions.act_window']
            
            rep_wiz_action_id = self.env['ir.model.data'].xmlid_to_res_id('eq_print.eq_print_wiz_action', raise_if_not_found=True)
            # rep_wiz_action_vals = act_window_obj.copy_data(rep_wiz_action_id)
            # rep_wiz_action_vals['name'] = self.name + ' Remote Print'
            # rep_wiz_action_vals['context'] = "{'report_name': '" + self.report_name + "' }"
            # new_rep_wiz_action_id = act_window_obj.create(rep_wiz_action_vals)
            # self.eq_report_wiz_action = new_rep_wiz_action_id
            # return new_rep_wiz_action_id

            # neu
            act = act_window_obj.browse(rep_wiz_action_id)
            # vals =  {
            #     'name': self.name + ' Remote Print',
            #     'context': "{'report_name': '" + self.report_name + "' }",
            # }
            copied_data_list = act.copy_data([])
            rep_wiz_action_vals = copied_data_list[0]
            rep_wiz_action_vals['name'] = self.name + ' Remote Print'
            rep_wiz_action_vals['context'] = "{'report_name': '" + self.report_name + "' }"
            new_rep_wiz_action_id = act_window_obj.create(rep_wiz_action_vals)
            self.eq_report_wiz_action = new_rep_wiz_action_id.id
            return new_rep_wiz_action_id.id
    
    @api.multi
    def _update_ir_values(self):
        for rep in self:
            if rep.eq_direct_print:
                action_id = rep._get_wiz_action()
                if rep.eq_ir_values_id:
                    rep.eq_ir_values_id.value = 'ir.actions.act_window,%s' % action_id
                    rep.eq_ir_values_id.name = rep.report_name + ' Remote Print'
                else:
                    current_value_id = self.env['ir.values'].search([('value', '=', 'ir.actions.report.xml,%s' % rep.id)])
                    if len(current_value_id):
                        rep.eq_ir_values_id = current_value_id.id
                        rep.eq_ir_values_id.value = 'ir.actions.act_window,%s' % action_id
                        rep.eq_ir_values_id.name = rep.name + ' Remote Print'
            else:
                if rep.eq_ir_values_id:
                    rep.eq_ir_values_id.unlink()
                    rep.eq_report_wiz_action.unlink()


    # def create(self, cr, uid, vals, context = None):
    def create(self, vals):
        res = super(eq_ir_actions_report_xml, self).create(vals)
        self._update_ir_values()
        return res
 
    @api.multi
    def write(self, vals):
        res = super(eq_ir_actions_report_xml, self).write(vals)
        self._update_ir_values()
        return res
