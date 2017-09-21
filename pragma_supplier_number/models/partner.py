# -*- coding: utf-8 -*-

##############################################################################
#
#    odoo (formerly known as OpenERP), Open Source Business Applications
#    Copyright (C) 2012-now Josef Kaser (<http://www.pragmasoft.de>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _name = _inherit

    supplier_number = fields.Char(compute='_get_supplier_number', inverse='_set_supplier_number',
                                  string=_('Supplier Number'), store=False)
    supp_auto_ref = fields.Char(_('Supplier Reference (automatically assigned)'), readonly=True, invisible=True)
    supp_no_auto_ref = fields.Char(_('Supplier Reference (manually assigned)'), readonly=True, invisible=True)
    supp_ref_print = fields.Char(_('Supplier Reference (used in reports)'), readonly=True, invisible=True)
    auto_supplier_ref = fields.Boolean(compute='_auto_supplier_ref', store=False, readonly=True, invisible=True)

    @api.one
    @api.depends('supp_auto_ref', 'supp_no_auto_ref')
    def _get_supplier_number(self):
        default_auto_supplier_ref = self.env['ir.values'].get_default('res.partner', 'default_auto_supplier_ref')
        auto_supplier_ref_by_account = self.env['ir.values'].get_default('res.partner',
                                                                         'auto_supplier_ref_by_account')

        company_id = self.env.user.company_id
        prop_account_payable = self.env['ir.property'].search(
            [('company_id', '=', company_id.id), ('name', '=', 'property_account_payable_id'), ('res_id', '=', False)])

        #### Anpassung Equitania - Fehler falls Standardkonten fehlen ###
        default_account_payable = None
        if prop_account_payable:
            default_account_payable = self.env['account.account'].browse(
                int(prop_account_payable.value_reference.split(',')[1]))

        for partner in self:
            if partner.supplier:
                if default_auto_supplier_ref:
                    #### Anpassung Equitania ###
                    if auto_supplier_ref_by_account and default_account_payable and partner.property_account_payable_id.code != default_account_payable.code:
                        partner.supplier_number = partner.property_account_payable_id.code

                        if not partner.supp_ref_print or partner.supp_ref_print <> partner.property_account_payable_id.code:
                            partner.write(
                                {
                                    'supp_ref_print': partner.property_account_payable_id.code
                                }
                            )

                    else:
                        _supp_auto_ref = partner.supp_auto_ref
                        partner.supplier_number = _supp_auto_ref

                        if not partner.supp_ref_print or partner.supp_ref_print != _supp_auto_ref:
                            partner.write(
                                {
                                    'supp_ref_print': _supp_auto_ref
                                }
                            )

                else:
                    _supp_no_auto_ref = partner.supp_no_auto_ref
                    partner.supplier_number = _supp_no_auto_ref

                    if not partner.supp_ref_print or partner.supp_ref_print != _supp_no_auto_ref:
                        partner.write(
                            {
                                'supp_ref_print': _supp_no_auto_ref,
                            }
                        )

    @api.multi
    def _set_supplier_number(self):
        for partner in self:
            partner.supp_no_auto_ref = partner.supplier_number

    @api.depends('supplier')
    def _auto_supplier_ref(self):
        default_auto_supplier_ref = self.env['ir.values'].get_default('res.partner', 'default_auto_supplier_ref')

        for partner in self:
            if partner.supplier:
                if default_auto_supplier_ref:
                    partner.auto_supplier_ref = default_auto_supplier_ref
                else:
                    partner.auto_supplier_ref = False

    # wird im View verwendet, um die Nummer nachträglich erzeugen zu können (wenn z.B. ein bestehender Kunde zum Lieferanten wird)
    @api.multi
    def create_supplier_number(self):
        self.ensure_one()

        vals = {}

        for partner in self:
            # wenn es eine übergeordnete Firma gibt
            if partner.parent_id:
                # und die eine Lieferantenummer hat
                if partner.parent_id.supp_auto_ref:
                    # dann die Lieferantennummer der übergeordneten Firma übernehmen
                    vals['supp_auto_ref'] = partner.parent_id.supp_auto_ref
                    vals['supp_no_auto_ref'] = partner.parent_id.supp_no_auto_ref
                    vals['supp_ref_print'] = partner.parent_id.supp_ref_print
            # in allen anderen Fällen
            else:
                # eine Lieferantennummer erzeugen
                vals['supp_auto_ref'] = self.env['ir.sequence'].get('supplier.number')
                vals['supp_no_auto_ref'] = vals['supp_auto_ref']
                vals['supp_ref_print'] = vals['supp_auto_ref']

            partner.write(vals)

    @api.model
    def create(self, vals):
        parent_id = None

        if 'parent_id' in vals:
            parent_id = self.env['res.partner'].browse([vals['parent_id']])

        if 'supplier' in vals:
            if vals['supplier']:
                # wenn es keine übergeordnete Firma gibt, dann eine Lieferantennummer erzeugen
                if not parent_id:
                    vals['supp_auto_ref'] = self.env['ir.sequence'].get('supplier.number')
                    vals['supp_ref_print'] = vals['supp_auto_ref']
                # sonst die Lieferantennummer der übergeordneten Firma übernehmen
                else:
                    vals['supp_auto_ref'] = parent_id['supplier_number']
                    vals['supp_ref_print'] = vals['supp_auto_ref']

        return super(ResPartner, self).create(vals)

    @api.multi
    def write(self, vals):
        parent = False

        if 'parent_id' in vals and vals['parent_id']:
            parent = vals['parent_id']

        # wenn es eine übergeordnete Firma gibt, dann die Lieferantennummer der übergeordneten Firma übernehmen
        if parent:
            partner_obj = self.env['res.partner']
            parent = partner_obj.browse([parent])

            if parent['supplier']:
                vals['supp_auto_ref'] = parent['supplier_number']
                vals['supp_ref_print'] = vals['supp_auto_ref']
            else:
                vals['supp_auto_ref'] = False
                vals['supp_ref_print'] = vals['supp_auto_ref']

        return super(ResPartner, self).write(vals)
