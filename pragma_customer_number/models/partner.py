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

    customer_number = fields.Char(compute='_get_customer_number', inverse='_set_customer_number',
                                  string=_('Customer Number'), store=False)
    cust_auto_ref = fields.Char(_('Customer Reference (automatically assigned)'), readonly=True, invisible=True)
    cust_no_auto_ref = fields.Char(_('Customer Reference (manually assigned)'), readonly=True, invisible=True)
    cust_ref_print = fields.Char(_('Customer Reference (used in reports)'), readonly=True, invisible=True)
    auto_customer_ref = fields.Boolean(compute='_auto_customer_ref', store=False, readonly=True, invisible=True)

    @api.one
    @api.depends('cust_auto_ref', 'cust_no_auto_ref')
    def _get_customer_number(self):
        ir_values = self.env['ir.values']

        default_auto_customer_ref = ir_values.get_default('res.partner', 'default_auto_customer_ref')
        auto_customer_ref_by_account = ir_values.get_default('res.partner', 'auto_customer_ref_by_account')

        company_id = self.env.user.company_id

        prop_account_receivable = self.env['ir.property'].search(
            [('company_id', '=', company_id.id), ('name', '=', 'property_account_receivable_id'),
             ('res_id', '=', False)])

        default_account_receivable = False

        #### Anpassung Equitania - Fehler falls Standardkonten fehlen ####
        if prop_account_receivable:
            default_account_receivable = self.env['account.account'].browse(
                int(prop_account_receivable.value_reference.split(',')[1]))

        for partner in self:
            if partner.customer:
                if default_auto_customer_ref:
                    #### Anpassung Equitania ####
                    if auto_customer_ref_by_account and default_account_receivable and partner.property_account_receivable_id.code != default_account_receivable.code:
                        partner.customer_number = partner.property_account_receivable_id.code

                        if not partner.cust_ref_print or partner.cust_ref_print != partner.property_account_receivable_id.code:
                            self.write(
                                {
                                    'cust_ref_print': partner.property_account_receivable_id.code
                                }
                            )

                    else:
                        _cust_auto_ref = partner.cust_auto_ref
                        partner.customer_number = _cust_auto_ref

                        if not partner.cust_ref_print or partner.cust_ref_print != _cust_auto_ref:
                            self.write(
                                {
                                    'cust_ref_print': _cust_auto_ref
                                }
                            )

                else:
                    _cust_no_auto_ref = partner.cust_no_auto_ref
                    partner.customer_number = _cust_no_auto_ref

                    if not partner.cust_ref_print or partner.cust_ref_print != _cust_no_auto_ref:
                        self.write(
                            {
                                'cust_ref_print': _cust_no_auto_ref
                            }
                        )

    @api.multi
    def _set_customer_number(self):
        for partner in self:
            partner.cust_no_auto_ref = partner.customer_number

    @api.depends('customer')
    def _auto_customer_ref(self):
        default_auto_customer_ref = self.env['ir.values'].get_default('res.partner', 'default_auto_customer_ref')

        for partner in self:
            if partner.customer:
                if default_auto_customer_ref:
                    partner.auto_customer_ref = default_auto_customer_ref
                else:
                    partner.auto_customer_ref = False

    # wird im View verwendet, um die Nummer nachträglich erzeugen zu können (wenn z.B. ein bestehender Lieferant zum Kunden wird)
    @api.multi
    def create_customer_number(self):
        self.ensure_one()

        vals = {}

        for partner in self:
            # wenn es eine übergeordnete Firma gibt
            if partner.parent_id:
                # und die eine Kundenummer hat
                if partner.parent_id.cust_auto_ref:
                    # dann die Kundennummer der übergeordneten Firma übernehmen
                    vals['cust_auto_ref'] = partner.parent_id.cust_auto_ref
                    vals['cust_no_auto_ref'] = partner.parent_id.cust_no_auto_ref
                    vals['cust_ref_print'] = partner.parent_id.cust_ref_print
            # in allen anderen Fällen
            else:
                # eine Kundennummer erzeugen
                vals['cust_auto_ref'] = self.env['ir.sequence'].get('customer.number')
                vals['cust_no_auto_ref'] = vals['cust_auto_ref']
                vals['cust_ref_print'] = vals['cust_auto_ref']

            partner.write(vals)

    @api.model
    def create(self, vals):
        parent_id = None

        if 'parent_id' in vals:
            parent_id = self.env['res.partner'].browse([vals['parent_id']])

        if 'customer' in vals:
            if vals['customer']:
                # wenn es keine übergeordnete Firma gibt, dann eine Kundennummer erzeugen
                if not parent_id:
                    vals['cust_auto_ref'] = self.env['ir.sequence'].get('customer.number')
                    vals['cust_ref_print'] = vals['cust_auto_ref']
                # sonst die Kundennummer der übergeordneten Firma übernehmen
                else:
                    vals['cust_auto_ref'] = parent_id['customer_number']
                    vals['cust_ref_print'] = vals['cust_auto_ref']

        return super(ResPartner, self).create(vals)

    @api.multi
    def write(self, vals):
        parent = False

        if 'parent_id' in vals and vals['parent_id']:
            parent = vals['parent_id']

        # wenn es eine übergeordnete Firma gibt, dann die Kundennummer der übergeordneten Firma übernehmen
        if parent:
            partner_obj = self.env['res.partner']

            parent = partner_obj.browse([parent])

            if parent['customer']:
                vals['cust_auto_ref'] = parent['customer_number']
                vals['cust_ref_print'] = vals['cust_auto_ref']
            else:
                vals['cust_auto_ref'] = False
                vals['cust_ref_print'] = vals['cust_auto_ref']

        return super(ResPartner, self).write(vals)


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        self = self.with_context(is_user=True)
        res = super(ResUsers, self).create(vals)
        return res