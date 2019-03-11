# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class eq_res_company(models.TransientModel):
    _inherit = 'base.config.settings'

    @api.multi
    def get_default_eq_report_logo(self, fields):

        user = self.env['res.users'].browse(self._uid)
        found_company = False
        if user:
            found_company = user.company_id

        if found_company:
            result = found_company.eq_report_logo
            if result:
                return {'eq_report_logo': result}
        return {'eq_report_logo': None}

    @api.multi
    def set_eq_report_logo(self):
        for record in self:
            record.company_id.eq_report_logo = record.eq_report_logo

    eq_report_logo = fields.Binary('Company Report Logo')
