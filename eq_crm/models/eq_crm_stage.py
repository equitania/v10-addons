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