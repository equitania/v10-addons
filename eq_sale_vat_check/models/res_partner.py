# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
import logging
from odoo.exceptions import ValidationError
import string

_logger = logging.getLogger(__name__)

_ref_vat = {
        'at': 'ATU12345675',
        'be': 'BE0477472701',
        'bg': 'BG1234567892',
        'ch': 'CHE-123.456.788 TVA or CH TVA 123456',  # Swiss by Yannick Vaucher @ Camptocamp
        'cy': 'CY12345678F',
        'cz': 'CZ12345679',
        'de': 'DE123456788',
        'dk': 'DK12345674',
        'ee': 'EE123456780',
        'el': 'EL12345670',
        'es': 'ESA12345674',
        'fi': 'FI12345671',
        'fr': 'FR32123456789',
        'gb': 'GB123456782',
        'gr': 'GR12345670',
        'hu': 'HU12345676',
        'hr': 'HR01234567896',  # Croatia, contributed by Milan Tribuson
        'ie': 'IE1234567FA',
        'it': 'IT12345670017',
        'lt': 'LT123456715',
        'lu': 'LU12345613',
        'lv': 'LV41234567891',
        'mt': 'MT12345634',
        'mx': 'MXABC123456T1B',
        'nl': 'NL123456782B90',
        'no': 'NO123456785',
        'pe': 'PER10254824220 or PED10254824220',
        'pl': 'PL1234567883',
        'pt': 'PT123456789',
        'ro': 'RO1234567897',
        'se': 'SE123456789701',
        'si': 'SI12345679',
        'sk': 'SK0012345675',
        'tr': 'TR1234567890 (VERGINO) veya TR12345678901 (TCKIMLIKNO)'  # Levent Karakas @ Eska Yazilim A.S.
    }

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.constrains("vat")
    def check_vat(self):
        return True

    @api.multi
    def eq_check_vat(self, vat):
        if self.env.context.get('company_id'):
            company = self.env['res.company'].browse(self.env.context['company_id'])
        else:
            company = self.env.user.company_id
        if company.vat_check_vies:
            # force full VIES online check
            check_func = self.vies_vat_check
        else:
            # quick and partial off-line checksum validation
            check_func = self.simple_vat_check
        for partner in self:
            if not vat:
                return _("VAT Number is required.")
            vat_country, vat_number = self._split_vat(vat)
            if not check_func(vat_country, vat_number):
                _logger.info("Importing VAT Number [%s] is not valid !" % vat_number)
                msg = partner._construct_constraint_msg(vat)
                return msg
        return False

    def _construct_constraint_msg(self,vat):
        self.ensure_one()

        def default_vat_check(cn, vn):
            # by default, a VAT number is valid if:
            #  it starts with 2 letters
            #  has more than 3 characters
            return len(cn) == 2 and cn[0] in string.ascii_lowercase and cn[1] in string.ascii_lowercase

        vat_country, vat_number = self._split_vat(vat)
        vat_no = "'CC##' (CC=Country Code, ##=VAT Number)"
        if default_vat_check(vat_country, vat_number):
            vat_no = _ref_vat[vat_country] if vat_country in _ref_vat else vat_no
            if self.env.context.get('company_id'):
                company = self.env['res.company'].browse(self.env.context['company_id'])
            else:
                company = self.env.user.company_id
            if company.vat_check_vies:
                return '\n' + _('The VAT number [%s] for partner [%s] either failed the VIES VAT validation check or did not respect the expected format %s.') % (vat, self.name, vat_no)
        return '\n' + _('The VAT number [%s] for partner [%s] does not seem to be valid. \nNote: the expected format is %s') % (vat, self.name, vat_no)

    # Validate the vat for the customer
    @api.multi
    def write(self,vals):
        if vals.get("vat","") != "":
            vat = vals.get("vat")
        else:
            vat = self.vat
        if vals.get("property_account_position_id",False):
            id = vals.get("property_account_position_id")
            property_account_position_id = self.env["account.fiscal.position"].search([("id","=",id)])
            if property_account_position_id.eq_check_vat:
                msg = self.eq_check_vat(vat)
                if msg:
                    raise ValidationError(msg)
        elif self.property_account_position_id and self.property_account_position_id.eq_check_vat:
            msg = self.eq_check_vat(vat)
            if msg:
                raise ValidationError(msg)
        return super(ResPartner, self).write(vals)

    # Validate the vat for the customer
    @api.model
    def create(self, vals):
        if vals.get("vat",False):
            vat = vals.get("vat")
        else:
            vat = False
        if vals.get("property_account_position_id",False):
            id = vals.get("property_account_position_id")
            property_account_position_id = self.env["account.fiscal.position"].search([("id","=",id)])
            if property_account_position_id.eq_check_vat:
                msg = self.eq_check_vat(vat)
                if msg:
                    raise ValidationError(msg)
        result = super(ResPartner, self).create(vals)
        return result
