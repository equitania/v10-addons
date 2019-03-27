# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

class res_partner(models.Model):
    _inherit = 'res.partner'


    eq_planned_date_type_purchase = fields.Selection([('cw', 'Calendar week'), ('date', 'Date')],
                                                  string="Planned Date Purchase",
                                                  help="If nothing is selected, the default from the settings will be used.")