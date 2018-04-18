# -*- coding: utf-8 -*-
# (c) 2015 Incaser Informatica S.L. - Sergio Teruel
# (c) 2015 Incaser Informatica S.L. - Carlos Dauden
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


from odoo import api, fields, models, _

class ProjectProject(models.Model):
    _inherit = 'project.project'

    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['project.task.type'].search([])
        return stage_ids

    stage_id = fields.Many2one('project.task.type', group_expand='_read_group_stage_ids')






