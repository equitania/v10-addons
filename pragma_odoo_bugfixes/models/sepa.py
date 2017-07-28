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

from odoo import api, models, fields, _


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'
    _name = _inherit

    def process_reconciliation(self, counterpart_aml_dicts=None, payment_aml_rec=None, new_aml_dicts=None):
        valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-?:().,'+ "
        orig = self.name

        clean = ''.join(c for c in orig if c in valid_chars)

        self.name = clean[:140]

        super(AccountBankStatementLine, self).process_reconciliation(counterpart_aml_dicts=counterpart_aml_dicts,
                                                                     payment_aml_rec=payment_aml_rec,
                                                                     new_aml_dicts=new_aml_dicts)

    @api.multi
    def process_reconciliations(self, data):
        valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-?:().,'+ "

        if type(data) == list:
            for elem in data:
                if type(elem) == dict and elem.has_key('new_aml_dicts'):
                    for entry in elem['new_aml_dicts']:
                        if entry.has_key('name') and entry['name']:
                            clean = ''.join(c for c in entry['name'] if c in valid_chars)
                            entry['name'] = clean[:140]

        super(AccountBankStatementLine, self).process_reconciliations(data)

class AccountPayment(models.Model):
    _inherit = "account.payment"
    _name = _inherit

    @api.one
    @api.constrains('payment_method_id', 'communication')
    def _check_communication_sepa(self):
        if self.payment_method_id == self.env.ref('account_sepa.account_payment_method_sepa_ct'):
            if len(self.communication) > 140:
                self.communication = self.communication[:140]

        super(AccountPayment, self)._check_communication_sepa()
