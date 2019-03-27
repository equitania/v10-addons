# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    eq_check_vat = fields.Boolean(string="Validate VAT")
