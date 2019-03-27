# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/

from odoo import api, models, fields

class report_stock_picking(models.Model):
    _inherit = 'stock.picking'

    def get_customer_product_code(self, partner, product):
        """
        Calculate customer product code
        :param partner: res.partner object
        :param product: product.product object
        :return: product customer code
        """
        product_customer_obj = self.env['product.customer.code'].search([('product_id','=',product.id),('partner_id','=',partner.id)])

        code = product_customer_obj.product_code

        if code:
            return str(code)
        else:
            return ''