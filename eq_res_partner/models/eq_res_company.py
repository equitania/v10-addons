# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

#Old API, Remove New API import if the Old API is used. Otherwise you'll get an import error.
from openerp import models, fields, api, _

class eq_res_company(models.Model):
    _inherit = 'res.company'

    eq_house_no = fields.Char(string="House Number",compute='_compute_address', inverse='_inverse_eq_house_no')

    def _compute_address(self):
        for company in self.filtered(lambda company: company.partner_id):
            address_data = company.partner_id.sudo().address_get(adr_pref=['contact'])
            if address_data['contact']:
                partner = company.partner_id.browse(address_data['contact']).sudo()
                company.street = partner.street
                company.eq_house_no = partner.eq_house_no
                company.street2 = partner.street2
                company.city = partner.city
                company.zip = partner.zip
                company.state_id = partner.state_id
                company.country_id = partner.country_id
                company.fax = partner.fax


    def _inverse_eq_house_no(self):
        for company in self:
            company.partner_id.eq_house_no = company.eq_house_no
