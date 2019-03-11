# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class eq_res_company(models.Model):
    _inherit = 'res.company'

    eq_report_logo = fields.Binary('Company Report Logo')
