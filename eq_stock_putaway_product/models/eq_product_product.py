# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # product_putaway_ids = fields.One2many(
    #     comodel_name='stock.product.putaway.strategy',
    #     inverse_name='product_product_id',
    #     string="Product stock locations")
    product_putaway_ids = fields.One2many(
        comodel_name='stock.product.putaway.strategy',
        related='product_tmpl_id.product_putaway_ids',
        string="Product stock locations")
