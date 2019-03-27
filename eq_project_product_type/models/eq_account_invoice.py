# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

class eq_project_account_invoice(models.Model):
    _inherit = 'account.invoice'

    eq_product_type_id = fields.Many2one('eq_product_type', string='Product Type')


class eq_project_account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'

    eq_product_type_id = fields.Many2one('eq_product_type', string='Product Type')
