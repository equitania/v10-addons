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


class GeneratorSettings(models.TransientModel):
    _inherit = 'account.config.settings'
    _name = _inherit

    default_auto_create = fields.Boolean(_('Autogenerate'), help=_('Autogenerate accounts for Persons'),
                                         default_model='res.partner')
    default_auto_customer_ref = fields.Boolean(_('Autogenerate Customer Reference'),
                                               help=_('Autogenerate customer numbers'), default_model='res.partner')
    auto_customer_ref_by_account = fields.Boolean(_('Create Customer Reference from Debitor Account'),
                                                  help=_('Create Customer Reference from Debitor Account'),
                                                  default_model='res.partner')
    default_auto_supplier_ref = fields.Boolean(_('Autogenerate Supplier Reference'),
                                               help=_('Autogenerate supplier numbers'), default_model='res.partner')
    auto_supplier_ref_by_account = fields.Boolean(_('Create Supplier Reference from Creditor Account'),
                                                  help=_('Create Supplier Reference from Creditor Account'),
                                                  default_model='res.partner')
    receivable_parent_id = fields.Many2one('account.account', _('Parent'), help=_('Parent account'))
    payable_parent_id = fields.Many2one('account.account', _('Parent'), help=_('Parent account'))

    @api.multi
    def set_default_accounts(self):
        ir_values = self.env['ir.values']

        ir_values.set_default('res.partner', 'receivable_parent_id',
                              self.receivable_parent_id and self.receivable_parent_id.id or False)
        ir_values.set_default('res.partner', 'payable_parent_id',
                              self.payable_parent_id and self.payable_parent_id.id or False)
        ir_values.set_default('res.partner', 'default_auto_customer_ref', self.default_auto_customer_ref or False)
        ir_values.set_default('res.partner', 'default_auto_supplier_ref', self.default_auto_supplier_ref or False)
        ir_values.set_default('res.partner', 'auto_customer_ref_by_account', self.auto_customer_ref_by_account or False)
        ir_values.set_default('res.partner', 'auto_supplier_ref_by_account', self.auto_supplier_ref_by_account or False)

    @api.model
    def get_default_accounts(self, fields):
        ir_values = self.env['ir.values']

        receivable = ir_values.get_default('res.partner', 'receivable_parent_id')
        payable = ir_values.get_default('res.partner', 'payable_parent_id')
        default_customer_ref = ir_values.get_default('res.partner', 'default_auto_customer_ref')
        default_supplier_ref = ir_values.get_default('res.partner', 'default_auto_supplier_ref')
        customer_ref_by_account = ir_values.get_default('res.partner', 'auto_customer_ref_by_account')
        supplier_ref_by_account = ir_values.get_default('res.partner', 'auto_supplier_ref_by_account')

        return {
            'receivable_parent_id': receivable,
            'payable_parent_id': payable,
            'default_auto_customer_ref': default_customer_ref,
            'default_auto_supplier_ref': default_supplier_ref,
            'auto_customer_ref_by_account': customer_ref_by_account,
            'auto_supplier_ref_by_account': supplier_ref_by_account,
        }
