# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo Addon, Open Source Management Solution
#    Copyright (C) 2014-now Equitania Software GmbH(<http://www.equitania.de>).
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


class eq_hr_employee_document(models.Model):
    _inherit = 'hr.employee.document'

    @api.model
    def _create_sequence(self):
        """
        Function for document number sequence creation
        """
        self.env["ir.sequence"].create(
            {"name": "EQ Employee Documents", "code": "hr.employee.document", "prefix": "Document No.:", "padding": 5,
             "number_increment": 1,
             "numer_nex_actual": 1})


    @api.model
    def create(self, vals):
        """
        Overrided base create function for document number sequence creation
        :param vals: vals
        :return: result
        """
        vals['name'] = self.env['ir.sequence'].next_by_code('hr.employee.document')
        result = super(eq_hr_employee_document, self).create(vals)
        return result
