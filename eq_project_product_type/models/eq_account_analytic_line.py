# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

#New API, Remove Old API import if the New API is used. Otherwise you'll get an import error.
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class eq_account_analytic_line(models.Model):
    _inherit = 'account.analytic.line'

    eq_product_type_id = fields.Many2one('eq_product_type', string='Product Type', required=True)

    @api.model
    def create(self,vals):
        if 'eq_product_type_id' not in vals:
            if 'invoice' in self._context:
                vals['eq_product_type_id'] = self._context['invoice'].eq_product_type_id.id
        res = super(eq_account_analytic_line, self).create(vals)
        return res


    def invoice_cost_create(self, data=None):
        invoices = self.env['account.invoice']
        invoice_line_obj = self.env['account.invoice.line']
        analytic_line_obj = self.env['account.analytic.line']

        # use key (partner/account, company, currency)
        # creates one invoice per key
        invoice_grouping = {}

        currency_id = False
        # prepare for iteration on journal and accounts
        for line in self:
            key = (line.account_id.id,
                   line.account_id.company_id.id,
                   line.account_id.partner_id.property_product_pricelist.currency_id.id)
            invoice_grouping.setdefault(key, []).append(line)

        for (key_id, company_id, currency_id), analytic_lines in invoice_grouping.items():
            # key_id is an account.analytic.account
            account = analytic_lines[0].account_id
            partner = account.partner_id  # will be the same for every line
            if (not partner) or not (currency_id):
                raise UserError(_('Contract incomplete. Please fill in the Customer and Pricelist fields for %s.') % (
                                         account.name,))

            curr_invoice = self._prepare_cost_invoice(partner, company_id, currency_id, analytic_lines)

            invoice_context = dict(lang=partner.lang,
                                   force_company=company_id,
                                   # set force_company in context so the correct product properties are selected (eg. income account)
                                   company_id=company_id)  # set company_id in context, so the correct default journal will be selected



            # use key (product, uom, user, invoiceable, analytic account, journal type)
            # creates one invoice line per key
            invoice_lines_grouping = {}
            ir_values_obj = self.env['ir.values']
            #product_id = ir_values_obj.get_default('project.task', 'default_project_product')
            #product_id = self.product_id.id
            for analytic_line in analytic_lines:
                product_id = analytic_line.product_id.id
                account = analytic_line.account_id

                if not analytic_line.to_invoice:
                    raise UserError(_('Trying to invoice non invoiceable line for %s.') % (
                        analytic_line.product_id.name))

                key = (#analytic_line.product_id.id,
                       product_id,
                       analytic_line.product_uom_id.id,
                       analytic_line.user_id.id,
                       analytic_line.to_invoice.id,
                       analytic_line.account_id,
                       #analytic_line.journal_id.type   #TODO usar is_:timesheet o alguna ltre x dif el timesheet de les lnes de factura
                       )
                # We want to retrieve the data in the partner language for the invoice creation
                analytic_line = analytic_line.with_context(invoice_context)

                invoice_lines_grouping.setdefault(key, []).append(analytic_line)


            # finally creates the invoice line
            for (product_id, uom, user_id, factor_id,
                 account), lines_to_invoice in invoice_lines_grouping.items():
                for line_to_invoice in lines_to_invoice:
                    curr_invoice_line = self.with_context(invoice_context)._prepare_cost_invoice_line(product_id, uom, user_id, factor_id, account,
                                                                        line_to_invoice,
                                                                        #journal_type
                                                                        data)
                    exist_account_invoice = self.env['account.invoice'].search([('partner_id','=',partner.id),('state','=','draft'),('eq_product_type_id','=',line_to_invoice.eq_product_type_id.id)])

                    if len(exist_account_invoice) > 0:
                        last_invoice = exist_account_invoice[0]
                        curr_invoice_line['invoice_id'] = last_invoice.id
                        curr_invoice_line['eq_product_type_id'] = line_to_invoice.eq_product_type_id.id
                    else:
                        curr_invoice['eq_product_type_id'] = line_to_invoice.eq_product_type_id.id
                        curr_invoice['message_follower_ids'] = []
                        last_invoice = invoices.with_context(invoice_context).create(curr_invoice)
                        curr_invoice_line['invoice_id'] = last_invoice.id
                        curr_invoice_line['eq_product_type_id'] = line_to_invoice.eq_product_type_id.id

                    curr_invoice_line['eq_user_id'] = user_id
                    acc_invoice_obj = invoice_line_obj.create(curr_invoice_line)

                    line_to_invoice.write({'invoice_id': last_invoice.id,'eq_invoice_line_id': acc_invoice_obj.id})

            #analytic_line_obj.browse(map(lambda x: x.id, analytic_lines)).write({'invoice_id': last_invoice.id})
            last_invoice.compute_taxes()
            invoices |= last_invoice


        for obj in self:
            obj.write({'eq_storno_flag': False})
        return invoices
