# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class PragmaSaleOrderReport(models.AbstractModel):
    _name = 'report.eq_sale.eq_report_saleorder'

    @api.model
    def render_html(self, docids, data=None):
        sale_order = None
        partner = None
        company_partner = None
        ceo = None
        customer_number = None
        order_date = None

        company = self.env.user.company_id

        if company:
            company_partner = company.partner_id
            ceo = company.ps_ceo

        vat = company.vat

        # if self.env['res.partner.bank'].search_count(
        #         [('partner_id', '=', company_partner.id), ('company_id', '=', self.env.user.company_id.id),
        #          ('ps_print_on_reports', '=', True)]) == 0:
        #     raise ValidationError(_('Please select exactly one bank account to be printed on the report.'))
        #
        # if self.env['res.partner.bank'].search_count(
        #         [('partner_id', '=', company_partner.id), ('company_id', '=', self.env.user.company_id.id),
        #          ('ps_print_on_reports', '=', True)]) > 1:
        #     raise ValidationError(_('You can only select one bank account to be printed on the report.'))

        bank = self.env['res.partner.bank'].search(
            [('partner_id', '=', company_partner.id), ('company_id', '=', self.env.user.company_id.id),
             ('ps_print_on_reports', '=', True)])

        bank_iban = ''
        bank_bic = ''
        bank_name = ''

        if bank:
            bank_iban = bank.acc_number
            bank_bic = bank.bank_id.bic
            bank_name = bank.bank_id.name

        sale_order = self.env['sale.order'].browse(docids)

        if sale_order:
            partner = sale_order.partner_id

            if 'cust_ref_print' in partner and partner['cust_ref_print']:
                customer_number = partner['cust_ref_print']
            elif partner.parent_id and 'cust_ref_print' in partner.parent_id and partner.parent_id['cust_ref_print']:
                customer_number = partner['cust_ref_print']
            elif partner['ref']:
                customer_number = partner['ref']
            elif partner.parent_id and partner.parent_id['ref']:
                customer_number = partner.parent_id['ref']

            language = None

            # get the customer's language
            if partner.lang:
                language = self.env['res.lang'].search([('code', '=', partner.lang)])
            # if customer has set no language then use the settings of the logged in user
            elif self.env.user.partner_id.lang:
                language = self.env['res.lang'].search([('code', '=', self.env.user.partner_id.lang)])

            if sale_order.date_order:
                # format the order date in the found language's date format
                if language:
                    order_date = fields.Date.from_string(sale_order.date_order).strftime(language.date_format)
                # else print the date in the format as it is stored in the database
                else:
                    order_date = sale_order.date_order

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
            'doc_model': 'sale.order',
            'docs': sale_order,
            'print_name': print_name,
            'ceo': ceo,
            'vat': _('VAT: ') + vat,
            'bank_iban': _('IBAN: ') + bank_iban,
            'bank_bic': _('BIC: ') + bank_bic,
            'bank_name': bank_name,
            'customer_number': customer_number,
            'order_date': order_date,
        }

        return self.env['report'].render('eq_sale.eq_report_saleorder', docargs)


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _name = _inherit

    @api.multi
    def print_quotation(self):
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})

        res = self.env['report'].get_action(self, 'eq_sale.eq_report_saleorder')

        return res
