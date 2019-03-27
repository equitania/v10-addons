# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields

class EqResUsers(models.Model):
    """EqResUsers class inherited from ResUsers class"""
    _inherit = 'res.users'

    eq_printer_ids = fields.Many2many(
        string="Possible Printers",
        comodel_name="eq.printer",
        relation="eq_printer_users_rel",
        column1="user_id",
        column2="eq_printer_id")
    eq_default_printer_id = fields.Many2one(string="Default Printer", comodel_name="eq.printer")
