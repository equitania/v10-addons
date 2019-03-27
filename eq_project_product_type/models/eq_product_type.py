# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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
