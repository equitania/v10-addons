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
from odoo import api, models, fields

class eq_report_account_invoice(models.Model):
    _inherit = 'account.invoice'

    def get_customer_product_code(self, partner, product):
        """
        Calculate customer product code
        :param partner: res.partner object
        :param product: product.product object
        :return: product customer code
        """
        print"partner: ", partner
        print"product: ", product

        product_customer_obj = self.env['product.customer.code'].search([('product_id','=',product.id),('partner_id','=',partner.id)])
        print"product_customer_obj: ",product_customer_obj

        code = product_customer_obj.product_code

        print"code: ", code

        if code:
            return str(code)
        else:
            return ''