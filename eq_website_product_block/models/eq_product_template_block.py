# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class eq_product_template_block(models.Model):
    _inherit = "product.template"

    eq_website_description = fields.Html(translate=True)
    website_description = fields.Html(translate = True)
