# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

class EqProjectTask(models.Model):
    """ Inherited project.task model for changing
    the type of the fields from Datetime to Date """
    _inherit = 'project.task'

    date_start = fields.Date(string='Starting Date', default=fields.Datetime.now, index=True, copy=False)
    date_end = fields.Date(string='Ending Date', index=True, copy=False)
    date_assign = fields.Date(string='Assigning Date', index=True, copy=False, readonly=True)
    date_last_stage_update = fields.Date(string='Last Stage Update',
                                             default=fields.Datetime.now,
                                             index=True,
                                             copy=False,
                                             readonly=True)
