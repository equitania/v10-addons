# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class eq_module_template(models.Model):
    _inherit = 'res.company'

    eq_ceo_title = fields.Char('res.partner.title',translate=True)
    eq_ceo_01 = fields.Char('CEO 1')
    eq_ceo_02 = fields.Char('CEO 2')
    eq_ceo_03 = fields.Char('CEO 3')
