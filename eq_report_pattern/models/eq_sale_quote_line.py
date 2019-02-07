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
from openerp import models, fields, api, _

class eq_sale_quote_line(models.Model):
    _name = "eq.sale.quote.line"
    _inherit = "sale.quote.line"

    quote_id = fields.Many2one('eq.document.template', 'Quotation Template Reference', required=True, ondelete='cascade', index=True)


    @api.model
    def create(self, values):
        if values['quote_id'] == 1 :
            return super(eq_sale_quote_line, self).create(values)
        else:
            quote_id = values['quote_id']
            quote_tmpl_obj = self.env['eq.document.template'].search([('id','=',quote_id)])
            if len(quote_tmpl_obj):
                return super(eq_sale_quote_line, self).create(values)
            else:
                tmpl_pool = self.env['eq.document.template']
                create_vals = {
                    'number_of_days': 30,
                    'name': values['name'],
                    'website_description': values['website_description']
                }
                tmpl_obj = tmpl_pool.create(create_vals)
                values.update({'quote_id': tmpl_obj.id,})
                values = self._inject_quote_description(values)
                res = super(eq_sale_quote_line, self).create(values)
                return res

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.ensure_one()
        if self.product_id:
            if self.quote_id.eq_model == 'purchase.order':
                self.price_unit = self.product_id.standard_price
            else:
                self.price_unit = self.product_id.lst_price
            name = self.product_id.name_get()[0][1]
            if self.product_id.description_sale:
                name += '\n' + self.product_id.description_sale
            self.name = name
            self.product_uom_id = self.product_id.uom_id.id

    @api.onchange('product_uom_id')
    def _onchange_product_uom(self):
        if self.product_id and self.product_uom_id and self.quote_id.eq_model != 'purchase.order':
            self.price_unit = self.product_id.uom_id._compute_price(self.product_id.lst_price, self.product_uom_id)
