# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _

class eq_product_template(models.Model):
    _inherit = 'product.template'


    #Überschreibt Constraint aus product.template, sodass dieser immer wahr ist.

    _sql_constraints = [
        ('default_code_unique', 'check(1=1)', "This Product No. is already in use!"),
    ]


class eq_product_product(models.Model):
    _inherit = 'product.product'


    #Überschreibt Constraint aus product.template, sodass dieser immer wahr ist.

    _sql_constraints = [
        ('default_code_unique', 'check(1=1)', "This Product No. is already in use!"),
    ]
