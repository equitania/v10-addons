# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from datetime import datetime


class EqCrmStage(models.Model):
    _inherit = 'crm.stage'

    @api.model
    def eq_crm_stage_remove(self):
        """
        Function which remove base lead stage if is created again after removing from odoo backend
        """
        stages = []
        stages.append(self.env.ref('crm.stage_lead1', raise_if_not_found=False))
        stages.append(self.env.ref('crm.stage_lead2', raise_if_not_found=False))
        stages.append(self.env.ref('crm.stage_lead3', raise_if_not_found=False))
        stages.append(self.env.ref('crm.stage_lead4', raise_if_not_found=False))

        today = datetime.today().strftime('%Y-%m-%d')
        for stage in stages:
            if stage:
                create_date = datetime.strptime(stage.create_date, '%Y-%m-%d %H:%M:%S').date()
                if str(create_date) == today:
                    stage.unlink()