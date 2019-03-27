# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
import datetime

class report_account_invoice(models.Model):
    _inherit = 'account.invoice'

    eq_ref_number = fields.Char('Sale Order Referenc', size=64)

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

    def get_eq_payment_terms(self, language, currency_id):
        """
            Show payment terms with custom text using 2 kinds of placeholders.
            Date1 & Date2 = Placeholder for Date that will be calculated and replaced
            Value1 % Value2 = Placehold for Value that will be calculated and replaced
            @object: account.invoice object
            @language: actual language
            @currency_id: actual currency_id of given invoice
            @return: Return new string with formated & calculated date and prices
        """

        object = self
        return self.env['eq_report_helper'].get_eq_payment_terms(object, language, currency_id)

class StockMove(models.Model):
    _inherit = 'stock.move'

    sale_line_id = fields.Many2one(
            related='procurement_id.sale_line_id',
            string='Sale Order Line',
            readonly=True,
            store=True,
            ondelete='set null'
    )

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    move_ids = fields.One2many(
            comodel_name='stock.move',
            inverse_name='sale_line_id',
            string='Ralated Moves',
            readonly=True,
            ondelete='set null'
    )


class report_account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'

    eq_move_ids = fields.Many2many('stock.move', string="Move") #Notwendig bei Teillieferungen
    eq_move_id = fields.Many2one('stock.move', string="Move")   #Funktioniert, nur nicht bei Teillieferungen

    @api.multi
    def check_retoure(self, move):

        name = move.picking_id.name
        pack_operation = self.env['stock.pack.operation'].search([('picking_id', '=', move.picking_id.id), ('product_id', '=', move.product_id.id)])
        picking_obj = self.env['stock.picking'].search([('origin','=', name),('picking_type_code','=','incoming')])
        return_move = self.env['stock.move'].search([('picking_id','in',picking_obj._ids)])
        pack_operation_retours = self.env['stock.pack.operation'].search([('picking_id', 'in', picking_obj._ids), ('product_id', '=', move.product_id.id)])
        full_qty = 0

        if len(picking_obj) > 0:
            for r_move in return_move:
                if r_move.product_id.id == move.product_id.id:
                    if len(pack_operation) > 0:
                        if len(pack_operation_retours) > 0:
                            for pack_operation_retour in pack_operation_retours:
                                full_qty = full_qty + pack_operation_retour.qty_done
                            if pack_operation.qty_done <= full_qty:
                                return False
            return True
        else:
            return True

    @api.multi
    def get_subtotal(self, price_per_unit, discount, qty):
        """
        Berechnung des Preis pro Zeile
        :param price_per_unit:
        :param qty:
        :return:
        """
        if discount and discount != 0.0:
            #price = (discount/100) * price_per_unit * qty
            price = (price_per_unit - ((discount / 100) * price_per_unit)) * qty
        else:
            price = price_per_unit * qty
        return price

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


    @api.model
    def create(self, vals):
        """
            let's get original sequence no from deliverynote and save it for every position on delivery note
            @cr: cursor
            @use: actual user
            @vals: alle values to be saved
            @context: context
        """


        # use standard save functionality and save it

        res = super(report_account_invoice_line, self).create(vals)
        stock_move_list = []
        account_invoice_line = res
        sale_line_id = account_invoice_line.sale_line_ids.id
        sale_order_obj = account_invoice_line.sale_line_ids.order_id
        if len(sale_order_obj) > 0:
            incoterm_location = sale_order_obj.eq_incoterm_location
            account_invoice_obj = account_invoice_line.invoice_id
            vals = {
                'eq_incoterm_location': incoterm_location,
            }
            account_invoice_obj.write(vals)
        if sale_line_id:
            stock_move_objs = self.env['stock.move'].search([('sale_line_id', '=', sale_line_id),('state','=','done')])
            eq_invoices = account_invoice_line.sale_line_ids.order_id.invoice_ids
            eq_existing_move_ids = []
            for eq_invoice in eq_invoices:
                for eq_invoice_line in eq_invoice.invoice_line_ids:
                    if eq_invoice_line.eq_move_ids:
                        eq_existing_move_ids = eq_existing_move_ids + eq_invoice_line.eq_move_ids.ids
                    if eq_invoice_line.eq_move_id.ids:
                        eq_existing_move_ids.append(eq_invoice_line.eq_move_id.id)
            for stock_move_obj in stock_move_objs:
                if len(stock_move_obj.origin_returned_move_id) == 0 and stock_move_obj.id not in eq_existing_move_ids:
                    stock_move_list.append(stock_move_obj.id)
                    ################ Obsolete sobald Report angepasst wurde
                    res.update({'eq_move_id': stock_move_obj.id})
                    ################
                else:
                    pass

            if len(stock_move_list) > 0:
                res.update({'eq_move_ids': [(6, 0, stock_move_list)]})

        return res

class eq_report_extension_stock_picking(models.Model):
    _inherit = "stock.picking"

    eq_ref_number = fields.Char('Sale Order Referenc', size=64)

    @api.model
    def create(self, vals):
        """
            Adds the customer ref number to the picking list. Gets data from context which is set in the method action_ship_create of the sale.order
            @cr: cursor
            @user: actual user
            @vals: values to be saved - we'll append eq_ref_number here
            @context: context
            @return: result of super method
        """

        #print"self: ", self
        #print"vals: ", vals
        res = super(eq_report_extension_stock_picking, self).create(vals)
        sale_order_obj = res.eq_sale_order_id
        client_order_ref = sale_order_obj.client_order_ref

        res.update({'eq_ref_number': client_order_ref})

        return res


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