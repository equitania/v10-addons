# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api

class EqIrActionsReportXml(models.Model):
    """ EqIRActionsReportXml class inherited from IrActionsReportXml class"""
    _inherit = 'ir.actions.report.xml'

    eq_direct_print = fields.Boolean(string="Remote Print")
    eq_ir_values_id = fields.Many2one(string="Print Menu", comodel_name="ir.values")
    eq_report_wiz_action = fields.Many2one(
        string="Report Wizard Action",
        comodel_name="ir.actions.act_window")

    @api.onchange('report_type')
    def _onchange_report_type(self):
        super(EqIrActionsReportXml, self)._onchange_report_type()
        self.eq_direct_print = False

    @api.multi
    def _get_wiz_action(self):
        self.ensure_one()
        if self.eq_report_wiz_action:
            return self.eq_report_wiz_action.id
        else:
            act_window_obj = self.env['ir.actions.act_window']

            rep_wiz_action_id = self.env['ir.model.data']\
                .xmlid_to_res_id('eq_print.eq_print_wiz_action', raise_if_not_found=True)
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
                    current_value_id = self.env['ir.values'].search(
                        [('value', '=', 'ir.actions.report.xml,%s' % rep.id)])
                    if current_value_id:
                        rep.eq_ir_values_id = current_value_id.id
                        rep.eq_ir_values_id.value = 'ir.actions.act_window,%s' % action_id
                        rep.eq_ir_values_id.name = rep.name + ' Remote Print'
            else:
                if rep.eq_ir_values_id:
                    rep.eq_ir_values_id.unlink()
                    rep.eq_report_wiz_action.unlink()

    @api.model
    def create(self, vals):
        """
        Override create function for update ir values
        :param vals: vals
        :return: res
        """
        res = super(EqIrActionsReportXml, self).create(vals)
        self._update_ir_values()
        return res

    @api.multi
    def write(self, vals):
        """
        Override write method for update ir values
        :param vals: vals
        :return: res
        """
        res = super(EqIrActionsReportXml, self).write(vals)
        self._update_ir_values()
        return res
