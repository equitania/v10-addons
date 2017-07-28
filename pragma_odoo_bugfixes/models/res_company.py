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


class ResCompany(models.Model):
    _inherit = 'res.company'
    _name = _inherit

    def reflect_code_digits_change(self, digits):
        accounts = self.env['account.account'].search([('company_id', '=', self.id)], order='code asc')

        for account in accounts:
            if len(account.code) == digits:
                account.write(
                    {
                        'code': account.code.ljust(digits, '0')
                    }
                )
