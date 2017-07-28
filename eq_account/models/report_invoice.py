# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class report_account_invoice(models.Model):
    _inherit = 'account.invoice'


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
        Workaround für HTML-Texte: Autom. Inhalt nach Speichern ohne Inhalt <p><br></p>
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




class report_account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    def get_price(self, value, currency_id, language):
        """
        Formatierung eines Preises mit Berücksichtigung der Einstellung Dezimalstellen Sale Price Report
        :param value:
        :param currency_id:
        :param language:
        :return:
        """
        return self.env["eq_report_helper"].get_price(value, language, 'Sale Price Report [eq_sale]',
                                                      currency_id)

    @api.multi
    def get_qty(self, value, language):
        """
        Formatierung für Mengenangabe mit Berücksichtigung der Einstellung Dezimalstellen Sale Quantity Report
        :param value:
        :param language:
        :return:
        """
        return self.env["eq_report_helper"].get_qty(value, language, 'Sale Unit of Measure Report [eq_sale]')






# class EqInvoiceReport(models.AbstractModel):
#     _name = 'report.eq_account.eq_report_invoice'
#
#     @api.model
#     def render_html(self, docids, data=None):
#         partner = None
#         invoice_date = None
#
#         invoice = self.env['account.invoice'].browse(docids)
#
#         if invoice:
#             partner = invoice.partner_id
#
#             language = None
#
#             # get the customer's language
#             if partner.lang:
#                 language = self.env['res.lang'].search([('code', '=', partner.lang)])
#             # if customer has set no language then use the settings of the logged in user
#             elif self.env.user.partner_id.lang:
#                 language = self.env['res.lang'].search([('code', '=', self.env.user.partner_id.lang)])
#
#             if invoice.date_invoice:
#                 # format the invoice date in the found language's date format
#                 if language:
#                     invoice_date = fields.Date.from_string(invoice.date_invoice).strftime(language.date_format)
#                 # else print the date in the format as it is stored in the database
#                 else:
#                     invoice_date = invoice.date_invoice
#
#         print_name = None
#
#         if partner.company_type == 'company':
#             if partner.name:
#                 print_name = partner.name
#             else:
#                 print_name = partner.name
#         elif partner.company_type == 'person':
#             if partner.name:
#                 print_name = partner.name
#             else:
#                 print_name = partner.name
#
#         docargs = {
#             'doc_ids': docids,
#             'doc_model': 'account.invoice',
#             'docs': invoice,
#             'print_name': print_name,
#
#             'invoice_date': invoice_date,
#         }
#
#         return self.env['report'].render('eq_account.eq_report_invoice', docargs)
#
#
#
# class report_invoice(models.AbstractModel):
#     _name = 'report.eq_account.eq_report_invoice'
#     _inherit = 'report.abstract_report'
#     _template = 'eq_account.eq_report_invoice'
#     _wrapped_report_class = EqInvoiceReport
#
#     @api.model
#     def render_html(self, docids, data=None):
#         partner = None
#         invoice_date = None
#         print 'test'