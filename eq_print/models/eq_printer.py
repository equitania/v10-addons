# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields

class EqPrinter(models.Model):
    """New class EqPrinter"""
    _name = 'eq.printer'
    _rec_name = "eq_name"
    _order = "eq_name desc"

    eq_name = fields.Char(string="Printer Name", required=True)
    eq_user_ids = fields.Many2many(
        string="Users",
        comodel_name="res.users",
        relation="eq_printer_users_rel",
        column1="eq_printer_id",
        column2="user_id")
