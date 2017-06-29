# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class EqInvoiceReport(models.AbstractModel):
    _name = 'report.eq_account.eq_report_invoice'

    @api.model
    def render_html(self, docids, data=None):
        partner = None
        invoice_date = None

        invoice = self.env['account.invoice'].browse(docids)

        if invoice:
            partner = invoice.partner_id

            language = None

            # get the customer's language
            if partner.lang:
                language = self.env['res.lang'].search([('code', '=', partner.lang)])
            # if customer has set no language then use the settings of the logged in user
            elif self.env.user.partner_id.lang:
                language = self.env['res.lang'].search([('code', '=', self.env.user.partner_id.lang)])

            if invoice.date_invoice:
                # format the invoice date in the found language's date format
                if language:
                    invoice_date = fields.Date.from_string(invoice.date_invoice).strftime(language.date_format)
                # else print the date in the format as it is stored in the database
                else:
                    invoice_date = invoice.date_invoice

        print_name = None

        if partner.company_type == 'company':
            if partner.name:
                print_name = partner.name
            else:
                print_name = partner.name
        elif partner.company_type == 'person':
            if partner.name:
                print_name = partner.name
            else:
                print_name = partner.name

        docargs = {
            'doc_ids': docids,
            'doc_model': 'account.invoice',
            'docs': invoice,
            'print_name': print_name,

            'invoice_date': invoice_date,
        }

        return self.env['report'].render('eq_account.eq_report_invoice', docargs)



class report_invoice(models.AbstractModel):
    _name = 'report.eq_account.eq_report_invoice'
    _inherit = 'report.abstract_report'
    _template = 'eq_account.eq_report_invoice'
    _wrapped_report_class = EqInvoiceReport

