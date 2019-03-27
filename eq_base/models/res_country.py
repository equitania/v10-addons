# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _

class res_country(models.Model):
    _inherit = 'res.country'

    eq_active = fields.Boolean(string = "Active", default = True)