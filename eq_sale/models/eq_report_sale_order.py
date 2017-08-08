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

# import time
# from openerp.osv import osv
# from openerp.report import report_sxw
from odoo import api, models, fields
#
# class eq_report_sale_order(report_sxw.rml_parse):
#
#     price = 0
#     data_dict = {}
#     display_gross_price = False
#
#
#
#     @api.model
#     def __init__(self):
#
#         # self.price = 0
#         # self.data_dict = {}
#         # self.display_gross_price = False
#         #
#         # super(eq_report_sale_order, self).__init__(cr, uid, name, context=context)
#         print 'init'
#         self.localcontext.update({
#             #'get_qty':self.get_qty,
#             'get_price': self.get_price,
#             #'get_standard_price': self.get_standard_price,
#             #'append_price': self.append_price,
#             #'calculate': self.calculate,
#             #'get_gross_price': self.get_gross_price,
#             #'get_gross_price_as_float': self.get_gross_price_as_float,
#             #'check_if_display_gross_price': self.check_if_display_gross_price,
#             #'calculate_sum': self.calculate_sum,
#             #'get_user_infos': self.get_user_infos,
#             #'get_user_signature': self.get_user_signature,
#             'get_tax': self.get_tax,
#             'has_tax_amount': self.has_tax_amount,
#             'test': self.test,
#         })
#
#     def test(self):
#         print 'in test2'
#         return "test123"
#
#     def get_tax(self, object, tax_id, language, currency_id):
#         amount_net = 0;
#         for line in object.order_line:
#             if tax_id.id in [x.id for x in line.tax_id] and not line.eq_optional:
#                  amount_net += line.price_subtotal
#
#         tax_amount = 0
#         for tex in self.env['account.tax']._compute([tax_id], amount_net, 1):
#             tax_amount += tex['amount']
#
#         return self.env["eq_report_helper"].get_price(tax_amount, language, 'Sale Price Report', currency_id)
#
#     def has_tax_amount(self, object, tax_id):
#         amount_net = 0;
#         for line in object.order_line:
#             if tax_id.id in [x.id for x in line.tax_id] and not line.eq_optional:
#                  amount_net += line.prireport_invoice_document_inherit_sale_stockce_subtotal
#
#         tax_amount = 0
#         for tex in self.env['account.tax']._compute([tax_id], amount_net, 1):
#             tax_amount += tex['amount']
#
#         if tax_amount > 0:
#             return True
#         return False
#
#     #def get_qty(self, object, language):
#     #    return self.pool.get("eq_report_helper").get_qty(self.cr, self.uid, object, language, 'Sale Quantity Report')
#
#     def get_price(self, object, language, currency_id):
#         return 0
#         # return self.env["eq_report_helper"].get_price(self.cr, self.uid, object, language, 'Sale Price Report', currency_id)
#
#     # def get_standard_price(self, object, language, currency_id):
#     #     return self.pool.get("eq_report_helper").get_standard_price(self.cr, self.uid, object, language, currency_id)
#     #
#     # def check_if_display_gross_price(self, object):
#     #     """
#     #         Check if we should display gross price
#     #         @object: order position
#     #         @return: True = display gross price
#     #     """
#     #     return self.pool.get("eq_report_helper").check_if_display_gross_price(self.cr, self.uid, object)
#     #
#     # """
#     # def check_if_display_gross_price(self, oinvoice_printbject):
#     #     self.display_gross_price =  self.pool.get("eq_report_helper").check_if_display_gross_price(self.cr, self.uid, object)
#     #     return self.display_gross_price
#     # """
#     #
#     # def get_gross_price(self, object, language, currency_id):
#     #     """
#     #         Get gross price for given order position together with currency
#     #         @object: Order positioninvoice_print
#     #         @language: Actual language
#     #         @currency_id: Currency id
#     #         @return: Gross price as string together with currency
#     #     """
#     #     return self.pool.get("eq_report_helper").get_gross_price(self.cr, self.uid, object, language, currency_id)
#     #
#     # def get_gross_price_as_float(self, object, language, currency_id):
#     #     """
#     #         Get gross price for given order position as float
#     #         @object:
#     #         @language:
#     #         @currency_id:
#     #         @return: Gross price as float
#     #     """
#     #     return self.pool.get("eq_report_helper").get_gross_price_as_float(self.cr, self.uid, object, language, currency_id)
#     #report_saleorder
#     # def get_user_infos(self):
#     #     """
#     #         Get user info (name + phone)
#     #         @cr: cursor
#     #         @uid: user id
#     #         @context: context
#     #         @return: user info (name + phone)
#     #     """
#     #     return self.pool.get("eq_report_helper").get_user_infos(self.cr, self.uid, self.uid)
#     #
#     # def get_user_signature(self):
#     #     """
#     #         Get user signature of actual logged user on odoo
#     #         @return: user signature
#     #     """
#     #     return self.pool.get("eq_report_helper").get_user_signature(self.cr, self.uid, self.uid)
#     #report_invoice_document_inherit_sale_stock
#     # def append_price(self, input_price, category_no):
#     #     """
#     #         Append price for category and save it
#     #         @input_price: Price to be saved
#     #         @category_no: Category no
#     #         @return: None - it's a void. We'll save all data in member variable
#     #     """
#     #     if category_no in self.data_dict:
#     #         value = self.data_dict[category_no]
#     #         value += input_price
#     #         self.data_dict[category_no] = value
#     #     else:
#     #         self.data_dict[category_no] = input_pricereport_saleorder
#     #
#     #     return None
#     #
#
#     def calculate_sum(self, input, category_no, lines):
#         """
#             Calculate sum - just a simple total price
#             @input: input
#             @category_no: category
#             @lines: order lines
#         """
#         result = 0
#
#         for line in lines:
#             if line.eq_optional is False:
#                 quantity = line.product_uom_qty
#                 price = line.price_unit
#                 result += quantity * price
#
#         return result
#     #
#     # def calculate(self, input, category_no):
#     #     """
#     #         Calculate total price without optional products
#     #         @input: Subtotal price - total inkl. optional products
#     #         @category_no: Category no
#     #         @return: Total price without optional products
#     #     """
#     #
#     #     if category_no in self.data_dict:               # check if we find total price for category
#     #         if self.display_gross_price is False:
#     #             total_price = self.data_dict[category_no]
#     #             result = input - total_price
#     #             return result
#     #         else:
#     #             total_price = self.data_dict[category_no]
#     #             result = input - total_price
#     #             return result
#     #
#     #     return input
#
#
# class report_lunchorder(models.AbstractModel):
#     # _name = 'report.sale.report_saleorder'
#     _name = 'report.eq_sale.eq_report_saleorder_document'
#     _inherit = 'report.abstract_report'
#     _template = 'eq_sale.eq_report_saleorder_document'
#     # _wrapped_report_class = eq_report_sale_order
#
#     @api.model
#     def render_html(self, docids, data=None):
#         print 'test'
#
#         sale_order = self.env['sale.order'].browse(docids)
#         docargs = {
#             'doc_ids': docids,
#             'doc_model': 'sale.order',
#             'docs': sale_order,
#             'customer_number': "TEST",
#             'test': self.test,
#         }
#
#         return self.env['report'].render('eq_sale.eq_report_saleorder', docargs)
#
#
#     def test(self):
#         print 'in test'
#         return  "test123"



class report_sale_order(models.Model):
    _inherit = 'sale.order'

    def get_tax(self, tax_id, language, currency_id):
        """
        Berechnet MwSt für die aktuelle Sprache und liefert den Wert zurück
        :param tax_id: MwSt-ID
        :param language: Aktuelle Sprache
        :param currency_id: Aktuelle Währung
        :return: MwSt für die aktuelle Sprache
        """
        amount_net = 0;
        for line in self.order_line:
            if tax_id.id in [x.id for x in line.tax_id] and not line.eq_optional:
                amount_net += line.price_subtotal

        tax_amount = 0
        for tex in self.env['account.tax']._compute([tax_id], amount_net, 1):
            tax_amount += tex['amount']

        return self.env["eq_report_helper"].get_price(tax_amount, language, 'Sale Price Report', currency_id)

    @api.multi
    def get_sum_without_optional_positions(self, category_id):
        """
        Berechnet die Zwischensumme der Positionen einer Kategorie und ignoriert dabei alle Positionen, die als OPTIONAL definiert sind
        :param category_positions: Alle Positionen einer Kategorie
        :return: Zwischensumme der Positionen einer Kategorie und ignoriert dabei alle Positionen, die als OPTIONAL definiert sind
        """
        return self.env["eq_report_helper"].get_sum_without_optional_positions(category_id)

    @api.multi
    def get_price(self, value, currency_id, language):
        """
        Formatierung eines Preises mit Berücksichtigung der Einstellung Dezimalstellen Sale Price Report
        :param value:
        :param currency_id:
        :param language:
        :return:
        """
        return self.env["eq_report_helper"].get_price(value, language, 'Sale Price Report', currency_id)

    @api.multi
    def get_qty(self, value, language):
        """
        Formatierung für Mengenangabe mit Berücksichtigung der Einstellung Dezimalstellen Sale Quantity Report
        :param value:
        :param language:
        :return:
        """
        return self.env["eq_report_helper"].get_qty(value, language, 'Sale Quantity Report')

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


class report_sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def get_price(self, value, currency_id, language):
        """
        Formatierung eines Preises mit Berücksichtigung der Einstellung Dezimalstellen Sale Price Report
        :param value:
        :param currency_id:
        :param language:
        :return:
        """
        return self.env["eq_report_helper"].get_price(value, language, 'Sale Price Report [eq_sale]', currency_id)

    @api.multi
    def get_qty(self, value, language):
        """
        Formatierung für Mengenangabe mit Berücksichtigung der Einstellung Dezimalstellen Sale Quantity Report
        :param value:
        :param language:
        :return:
        """
        return self.env["eq_report_helper"].get_qty(value, language, 'Sale Unit of Measure Report [eq_sale]')
