# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class eq_deliver_conditions(models.Model):
    _name = 'eq.delivery.conditions'
    _rec_name = 'eq_name'

    eq_name = fields.Char('Name', size=128)
