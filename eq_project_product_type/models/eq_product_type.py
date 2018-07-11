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

class eq_product_type(models.Model):
    _name = 'eq_product_type'
    _rec_name = 'eq_name'

    eq_name = fields.Char(string="Name")

    @api.model
    def generate_default_product_objects(self):
        """
         Generiert die Default-Objekte
        :return:
        """
        vals = {}
        vals.update({
            'eq_name': 'Odoo',
        })
        self.create(vals)

        vals.clear()

        vals.update({
            'eq_name': 'eNVenta',
        })
        self.create(vals)

        vals.clear()

        vals.update({
            'eq_name': 'ID Line',
        })
        self.create(vals)

        vals.clear()

        vals.update({
            'eq_name': 'Agorum',
        })
        self.create(vals)

        vals.clear()

        vals.update({
            'eq_name': 'EQ Arbeitsplatz',
        })
        self.create(vals)

        vals.clear()

        vals.update({
            'eq_name': 'Sonstiges',
        })
        self.create(vals)