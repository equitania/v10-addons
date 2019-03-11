# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _

class res_country(models.Model):
    _inherit = 'res.country'

    eq_active = fields.Boolean(string = "Active", default = True)