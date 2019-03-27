# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class eq_product_template_block(models.Model):
    _inherit = "product.template"

    eq_website_description = fields.Html(translate=True)
    website_description = fields.Html(translate = True)
