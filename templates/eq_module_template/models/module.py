# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class eq_module_template(models.Model):
    _name = 'eq_module_template'


    field_char = fields.Char('My Char Field')