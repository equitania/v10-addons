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

    auto_create = fields.Boolean('Autogenerate', help='Autogenerate accounts for Persons')
    default_auto_customer_ref = fields.Boolean('Set customer reference', help='Set customer reference')
    default_auto_supplier_ref = fields.Boolean('Set supplier reference', help='Set supplier reference')
    receivable_parent_id = fields.Many2one('account.account', 'Parent', help='Parent account')
    payable_parent_id = fields.Many2one('account.account', 'Parent', help='Parent account')
    auto_ref = fields.Boolean(compute='_is_auto_ref_generation_active', string=_('Automatic Customer umber'),
                              help=_('Autogenerate customer number'))

    """
    defaults = {
        'receivable_parent_id': lambda self: self.env['ir.values'].get_default('res.partner', 'receivable_parent_id'),
        'payable_parent_id': lambda self: self.env['ir.values'].get_default('res.partner', 'payable_parent_id'),
    }
    """

    @api.model
    def create(self, vals):
        defaults = self.default_get(['auto_create'])

        if 'is_lead' in self._context:
            if self._context['is_lead'] == True:
                vals.update({'customer': True})

        if 'is_user' in self._context:
            if self._context['is_user'] == True:
                vals.update({'customer': False})

        if 'auto_create' not in defaults or ('auto_create' in defaults and not bool(defaults['auto_create'])):
            return super(ResPartner, self).create(vals)

        if 'parent_id' in vals and bool(vals['parent_id']):
            return super(ResPartner, self).create(vals)

        if 'customer' in vals and vals['customer']:
            if not 'property_account_receivable_id' in vals or not vals['property_account_receivable_id'] or not self.is_correct_value(vals['property_account_receivable_id']):
                vals['property_account_receivable_id'] = self.create_account(vals, vals['name'], 'receivable', False)

        if 'supplier' in vals and vals['supplier']:
            if not 'property_account_payable_id' in vals or vals['property_account_payable_id'] or not self.is_correct_value(
                    vals['property_account_payable_id']):
                vals['property_account_payable_id'] = self.create_account(vals, vals['name'], 'payable', False)

        return super(ResPartner, self).create(vals)

    @api.multi
    def write(self, vals):
        for partner in self:
            defaults = self.default_get(['auto_create'])

            if 'auto_create' not in defaults or ('auto_create' in defaults and not bool(defaults['auto_create'])):
                return super(ResPartner, self).write(vals)

            if 'parent_id' in vals and bool(vals['parent_id']):
                super(ResPartner, self).write(vals)

            if isinstance(self, list) and len(self) == 1 or isinstance(self, long):
                # prüfen, ob das Ergebnis eine Liste ist; falls nicht, wurde mit browse() kein Eintrag gefunden (wenn z.B. aus einem Lead ein neuer Kunde angelegt wird)
                if 'customer' in vals and vals['customer']:
                    if partner.property_account_receivable_id and len(partner.property_account_receivable_id.code) != 5:
                        vals['property_account_receivable_id'] = self.create_account(vals, partner.name, 'receivable',
                                                                                  partner.ref)

                if 'supplier' in vals and vals['supplier']:
                    if partner.property_account_payable_id and len(partner.property_account_payable_id.code) != 5:
                        vals['property_account_payable_id'] = self.create_account(vals, partner.name, 'payable',
                                                                               partner.ref)
                break

        return super(ResPartner, self).write(vals)

    def is_correct_value(self, acc_id):
        account_object = self.env['account.account']
        account = account_object.browse(acc_id)

        if not bool(account):
            return False

        return len(account.code) == 5

    def is_code_valid(self, code, acctype):
        if acctype == 'receivable' and int(code) > 69999:
            raise ValidationError(_('Debitor account number is greater than 69999! Number is: %s') % (code))
        elif acctype == 'payable' and int(code) > 99999:
            raise ValidationError(_('Creditor account number is greater than 99999! Number is: %s') % (code))

    def account_exists(self, acctype, name):
        count = self.env['account.account'].search_count([('name', '=', name), ('user_type_id.type', '=', acctype)])

        return count != 0

    def get_account_type(self, acctype):
        account_type_id = self.env['account.account.type'].search([('type', '=', acctype)])

        if len(account_type_id):
            account_type_id = account_type_id[0]

        return account_type_id

    def update_values(self, acctype, vals, defaults):
        if (acctype + '_parent_id') not in defaults:
            raise ValidationError(_('Please set a default value for %s in Technical Settings/Accounting') % (acctype))

        parent_id = defaults[acctype + '_parent_id']

        if not acctype + '_parent_id' in vals:
            vals.update(
                {
                    acctype + '_parent_id': parent_id
                }
            )

        elif not vals[acctype + '_parent_id']:
            vals[acctype + '_parent_id'] = parent_id

        return vals

    def create_account(self, vals, name, acctype, ref):
        # FIXME:
        # Kontonummern nach der folgenden Logik vergeben:
        # - Schema: abbccc
        #    - a: 1 = Debitor, 7 = Kreditor
        #    - bb: Position (zweistellig) des ersten Zeichens im Kundennamen im String "alphabet"; wenn nicht gefunden, dann 00
        #    - ccc: lfd. Nr., muss für jedes bb gesondert gezählt werden => für jedes bb eigener Sequenzer (*2 für Debitoren und Kreditoren)
        # diesen Abschnitt nur verwenden, wenn ein entsprechender Parameter in ir.config_parameter gesetzt wurde (z.B. "inox.autocreate"), da er alles andere als allgemeingültig ist...
        """
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ1234567890"
        pos_value = alphabet.find(name[:1].upper()) + 1
        
        # wenn nix gefunden (z.B. Sonderzeichen), dann auf 0 setzen
        if pos_value == -1:
            pos_value = 0
        
        pos_formatted = '%02d' % (pos_value)
        
        next = self.env['ir.sequence'].get(acctype + '.sequence.number')
        code = next[:1] + pos_formatted + next[-2:]
        """

        code = self.env['ir.sequence'].get(acctype + '.account.number')
        defaults = self.default_get(['auto_ref'])  # Can be set in settings
        # if 'auto_ref' in defaults and bool(defaults['auto_ref']) and not ref and ('ref' in vals and not vals['ref'] or 'ref' not in vals):
        #     vals['ref'] = self.env['ir.sequence'].get('customer.sequence.number')
        self.is_code_valid(code, acctype)

        # EQ - unsere Version
        if 'company_name' in vals:
            if vals['company_name']:
                if 'eq_firstname' in vals:
                    if vals['eq_firstname']:
                        name = vals['company_name'] + ', ' + vals['eq_firstname'] + ' ' + name
                else:
                    name = vals['company_name'] + ', ' + name
            else:
                if 'eq_firstname' in vals:
                    if vals['eq_firstname']:
                        name = vals['eq_firstname'] + ' ' + name
        else:
            if 'eq_firstname' in vals:
                if vals['eq_firstname']:
                    name = vals['eq_firstname'] + ' ' + name

        if self.account_exists(acctype, name):
            raise ValidationError(_('An account for %s already exists!') % (name))

        account_type_id = self.get_account_type(acctype)
        default_values = self.env['res.partner'].default_get([acctype + '_parent_id'])
        vals = self.update_values(acctype, vals, default_values)
        parent_account = self.env['account.account'].browse(vals[acctype + '_parent_id'])

        data = {
            'code': code,
            'name': name,
            # 'type': acctype,
            'user_type_id': account_type_id.id,
            # 'parent_id': parent_account.id,
            'reconcile': True,
        }

        return self.env['account.account'].create(data)

    @api.depends
    def _is_auto_ref_generation_active(self):
        for line in self:
            line.auto_ref = self.env['ir.values'].get_default('res.partner', 'auto_ref')

class eqLead2OpportunityPartner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

    @api.multi
    def action_apply(self):
        """ Convert lead to opportunity or merge lead and opportunity and open
            the freshly created opportunity view.
        """
        self = self.with_context(is_lead=True)
        res = super(eqLead2OpportunityPartner, self).action_apply()
        return res



