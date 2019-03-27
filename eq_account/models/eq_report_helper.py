# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, _
import datetime

class eq_report_helper_account(models.TransientModel):
    
    _inherit = "eq_report_helper"

    def get_eq_payment_terms(self, object, language, currency_id):
        """
            Show payment terms with custom text using 2 kinds of placeholders.
            Date1 & Date2 = Placeholder for Date that will be calculated and replaced
            Value1 % Value2 = Placeholder for Value that will be calculated and replaced
            @object: account.invoice object
            @language: actual language
            @currency_id: actual currency_id of given invoice
            @return: Return new string with formated & calculated date and prices
        """

        # get details of selected payment term
        payment_term_line_obj = self.env['account.payment.term.line'].search([])
        payment_term_line_ids = self.env['account.payment.term.line'].search([('payment_id', '=', object.payment_term_id.id)])
        payment_term_obj = self.env['account.payment.term'].search([('id', '=', object.payment_term_id.id)])
        payment_term_result = payment_term_obj.note

        d1_set = False  # helper flag - true => date1 was set
        d2_set = False  # helper flag - true => date1 was set
        v1_set = False  # helper flag - true => value1 was set
        d1_set = False  # helper flag - true => value2 was set
        ignore_invoice_date = True

        # convert string to date
        if object.date_invoice:
            invoice_date_object = self._convert_string_to_date(object.date_invoice)
            ignore_invoice_date = False

        # let's get all payment termn lines for actual payment term, calculate date & value and replace result in our final text
        for line_id in payment_term_line_ids:
            line = payment_term_line_obj.search([('id','=',line_id.id)])

            if ignore_invoice_date is False:  # recalculate and set date only if an invoice date is provided
                recalculated_date = invoice_date_object + datetime.timedelta(days=line.days)
                date_format = self._get_date_format_for_language(language)

                # calculate date and replace it
                if d1_set is False:
                    if payment_term_result:
                        payment_term_result = payment_term_result.replace("[Date1]",
                                                                          recalculated_date.strftime(date_format))
                        d1_set = True
                else:

                    if payment_term_result:

                        payment_term_result = payment_term_result.replace("[Date2]",
                                                                          recalculated_date.strftime(date_format))
                        d2_set = True

            # calculate price and replace it
            if line.value_amount > 0:

                total_value = object.amount_total * line.value_amount
            else:

                total_value = object.amount_total

            # reformat price
            total_value = self.get_standard_price(total_value, language, currency_id)

            # and now set price...make sure that you set price for each placeholder
            if v1_set is False:

                if payment_term_result:

                    payment_term_result = payment_term_result.replace("[Value1]", total_value)
                    v1_set = True
            else:

                if payment_term_result:

                    payment_term_result = payment_term_result.replace("[Value2]", total_value)
                    v2_set = True


        return payment_term_result
