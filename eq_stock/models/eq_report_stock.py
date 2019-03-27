# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class report_stock_picking(models.Model):
    _inherit = 'stock.picking'

    # def get_tax(self, tax_id, language, currency_id):
    #     amount_net = 0;
    #     for line in self.order_line:
    #         if tax_id.id in [x.id for x in line.tax_id] and not line.eq_optional:
    #             amount_net += line.price_subtotal
    #
    #     tax_amount = 0
    #     for tex in self.env['account.tax']._compute([tax_id], amount_net, 1):
    #         tax_amount += tex['amount']
    #
    #     return self.env["eq_report_helper"].get_price(tax_amount, language, 'Sale Price Report', currency_id)
    #
    #
    # @api.multi
    # def get_price(self, value, currency_id, language):
    #     """
    #     Formatierung eines Preises mit Berücksichtigung der Einstellung Dezimalstellen Sale Price Report
    #     :param value:
    #     :param currency_id:
    #     :param language:
    #     :return:
    #     """
    #     return self.env["eq_report_helper"].get_price(value, language, 'Sale Price Report', currency_id)
    #
    # @api.multi
    # def get_qty(self, value, language):
    #     """
    #     Formatierung für Mengenangabe mit Berücksichtigung der Einstellung Dezimalstellen Sale Quantity Report
    #     :param value:
    #     :param language:
    #     :return:
    #     """
    #     return self.env["eq_report_helper"].get_qty(value, language, 'Sale Quantity Report')

    def check_show_quantity(self,product,picking):
        stock_ops = self.env['stock.pack.operation'].search([('product_id','=',product.id),('picking_id','=',picking.id)])
        if len(stock_ops) > 0:
            stock_op = stock_ops[0]
            if stock_op.qty_done > 0:
                return True
            else:
                return False
        return True

    @api.multi
    def html_text_is_set(self, value):
        """
        Workaround für HTML-Texte: Autom. Inhalt nach Speichern ohne Inhalt: <p><br></p>
        Entfernen der Zeilenumbrüche und Paragraphen für Test, ob ein Inhalt gesetzt wurde
        :param value:
        :return:
        """
        if not value:
            return False

        value = value.replace('<br>', '')
        value = value.replace('<p>', '')
        value = value.replace('</p>', '')
        value = value.replace('<', '')
        value = value.replace('>', '')
        value = value.replace('/', '')
        value = value.strip()
        return value != ''
