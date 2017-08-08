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

import time
import datetime

from odoo import api, models, _
# from openerp.report import report_sxw


class eq_report_helper(models.TransientModel):
    _name = "eq_report_helper"

    def get_qty(self, value, language, param_name):
        """
        Formatierung einer Mengenangabe
        :param value: Menge
        :param language:
        :param param_name: Name der Einstellung für die Dezimalstellen (decimal_precision)
        :return:
        """

        precision = self.env['decimal.precision'].precision_get(param_name)
        string = ("%%5.%df" % precision)
        result = (string % value)

        # parse string and generate correct number format
        result = self.reformat_string(result, precision, language)

        return result

    def get_price(self, value, language, param_name, currency_id=False):
        """
        Formatierung eines Preiswertes mit eingestellter Anzahl an Dezimalstellen und Berücksichtigung der Sprache
        :param value: Preis
        :param language:
        :param param_name: Name der Einstellung für die Dezimalstellen (decimal_precision)
        :param currency_id:
        :return:
        """
        precision = self.env['decimal.precision'].precision_get(param_name)
        string = ("%%5.%df" % precision)
        result = (string % value)

        # parse string and generate correct number format
        result = self.reformat_string(result, precision, language)
        # Currency Symbol is added
        if currency_id:
            result += (' %s' % currency_id.symbol)

        return result

    def get_standard_price(self, object, language, currency_id=False):
        """
            Price formater - formats given number to default price format 1.000,00
        """

        precision = 2
        string = ("%%5.%df" % precision)
        result = (string % object)
        result = self.reformat_string(result, precision, language)
        # Currency Symbol is added
        if currency_id:
            result += (' %s' % currency_id.symbol)

        return result

    def get_gross_price_invoice(self, object, language, currency_id=False):
        """
            Calculate gross price a return result as string together with currency back
            @object: order line object
            @currency_id: Currency
            @return: Calculated gross price
        """

        gross_price = object.price_unit * object.quantity
        return self.get_standard_price(gross_price, language, currency_id)

    def get_gross_price(self, object, language, currency_id=False):
        """
            Calculate gross price a return result as string together with currency back
            @object: order line object
            @currency_id: Currency
            @return: Calculated gross price
        """

        gross_price = object.price_unit * object.product_uom_qty
        return self.get_standard_price(gross_price, language, currency_id)

    def _convert_string_to_date(self, date_as_string):
        """
            Convert date in string format like '2016-02-09' into date
            @date_as_string: date in string format
            @return: string converted into date

        """
        return datetime.datetime.strptime(date_as_string, '%Y-%m-%d')

    def _get_date_format_for_language(self, lang_code):
        """
            Get date format for actual language
            @lang_code: actual language code
            @return: Date forma for actual language
        """
        lang_obj = self.env['res.lang']
        languages = lang_obj.search([('code', '=', lang_code)])
        if languages:
            return languages[0].date_format

        return ''

    # def get_eq_payment_terms(self, object, language, currency_id=False):
    #     """
    #         Show payment terms with custom text using 2 kinds of placeholders.
    #         Date1 & Date2 = Placeholder for Date that will be calculated and replaced
    #         Value1 % Value2 = Placehold for Value that will be calculated and replaced
    #         @object: account.invoice object
    #         @language: actual language
    #         @currency_id: actual currency_id of given invoice
    #         @return: Return new string with formated & calculated date and prices
    #     """
    #     payment_term_result = object.payment_term.note  # hold our result and return it back as final result
    #
    #     # get details of selected paycondition
    #     payment_term_line_obj = self.env['account.payment.term.line']
    #     payment_term_lines = payment_term_line_obj.search([('payment_id', '=', object.payment_term.id), ])
    #
    #     d1_set = False  # helper flag - true => date1 was set
    #     d2_set = False  # helper flag - true => date1 was set
    #     v1_set = False  # helper flag - true => value1 was set
    #     d1_set = False  # helper flag - true => value2 was set
    #     ignore_invoice_date = True
    #
    #     # convert string to date
    #     if object.date_invoice:
    #         invoice_date_object = self._convert_string_to_date(object.date_invoice)
    #         ignore_invoice_date = False
    #
    #     # let's get all payment termn lines for actual payment term, calculate date & value and replace result in our final text
    #     for line in payment_term_lines:
    #         if ignore_invoice_date is False:  # recalculate and set date only if an invoice date is provided
    #             recalculated_date = invoice_date_object + datetime.timedelta(days=line.days)
    #             date_format = self._get_date_format_for_language(language)
    #
    #             # calculate date and replace it
    #             if d1_set is False:
    #                 if payment_term_result:
    #                     payment_term_result = payment_term_result.replace("[Date1]",
    #                                                                       recalculated_date.strftime(date_format))
    #                     d1_set = True
    #             else:
    #                 if payment_term_result:
    #                     payment_term_result = payment_term_result.replace("[Date2]",
    #                                                                       recalculated_date.strftime(date_format))
    #                     d2_set = True
    #
    #         # calculate price and replace it
    #         if line.value_amount > 0:
    #             total_value = object.amount_total * line.value_amount
    #         else:
    #             total_value = object.amount_total
    #
    #         # reformat price
    #         total_value = self.get_standard_price(total_value, language, currency_id)
    #
    #         # and now set price...make sure that you set price for each placeholder
    #         if v1_set is False:
    #             if payment_term_result:
    #                 payment_term_result = payment_term_result.replace("[Value1]", total_value)
    #                 v1_set = True
    #         else:
    #             if payment_term_result:
    #                 payment_term_result = payment_term_result.replace("[Value2]", total_value)
    #                 v2_set = True
    #
    #     return payment_term_result


    def reformat_string(self, data, precision, language):
        """
            Creates formated number with count of decimal positions from odd and puts hardcoded thousand separator on right place.
            We can chane both tags for decimal separator and thousand separator in our variables
            @data: number as string formated from odoo
            @precision: count of decimal positions from odoo
        """

        res_lang_obj = self.env["res.lang"]
        langauge_record = res_lang_obj.search([("code", "=", language)])
        # langauge_record = res_lang_obj.browse(language_id[0])

        # print langauge_record


        DECIMAL_SEPARATOR_TAG = langauge_record.decimal_point
        THOUSAND_SEPARATOR_TAG = langauge_record.thousands_sep

        # DECIMAL_SEPARATOR_TAG = ","
        # THOUSAND_SEPARATOR_TAG = "."

        # replace . with ,
        data = data.replace(".", DECIMAL_SEPARATOR_TAG)

        # delete all white spaces
        data = data.replace(" ", "")

        # finalResult = data
        tempData = ""
        decimal_part = ""

        # extract decimal part in case, that we have one in our string
        if precision > 0:
            startIndex = data.find(DECIMAL_SEPARATOR_TAG);
            endIndex = len(data)

            # get decimal part...example 1256,85 -> decimal_part = ,85
            decimal_part = data[startIndex:endIndex]

            tempdata = data[0:startIndex]
            data = tempdata

        # iterate our numbre from end to start and set THOUSAND_SEPARATOR_TAG on right place
        index = len(data)
        counter = 0
        finalResult = ""
        while index > 0:
            if counter == 3:
                finalResult += THOUSAND_SEPARATOR_TAG
                counter = 0

            finalResult += data[index - 1]
            index = index - 1
            counter = counter + 1

        # we're done here, let's reverse our string to get back to normal number
        finalResult = finalResult[::-1]

        # append decimal_part if we have one
        if len(decimal_part) > 0:
            finalResult += decimal_part

        return finalResult

    def get_sum_without_optional_positions(self, category_positions):
        """
        Berechnet die Zwischensumme der Positionen einer Kategorie und ignoriert dabei alle Positionen, die als OPTIONAL definiert sind
        :param category_positions: Alle Positionen einer Kategorie
        :return: Zwischensumme der Positionen einer Kategorie und ignoriert dabei alle Positionen, die als OPTIONAL definiert sind
        """
        result = 0
        for position in category_positions:
            if position.eq_optional is False:                       # nur Positionen, die NICHT optional sind, sollen wir berücksichtigen
                result = result + position.price_subtotal

        return result