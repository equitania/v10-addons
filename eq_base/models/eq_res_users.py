# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class eq_res_users(models.Model):
    _inherit = 'res.users'

    eq_signature = fields.Binary(string='Signature')

