# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _

# Erweitert account.invoice
class eq_account_invoice(models.Model):
    _inherit = 'account.invoice'

    # Get default template
    def _get_default_template(self):
        eq_default = self.env["eq.document.template"].search([("eq_model", "=", "account.invoice"), ('eq_default', '=', True)],limit=1)
        if eq_default:
            return eq_default
   
    document_template_id = fields.Many2one(comodel_name='eq.document.template', string='Document Template',domain="['|',('eq_model', '=', False),('eq_model','=','account.invoice')]}",default=_get_default_template)#TODO: readonly falls Rechnung nicht mehr editierbar?
    comment = fields.Html('Additional Information')

    # @api.onchange('document_template_id')
    # def onchange_document_template_id(self):
    #     selected_template = self.document_template_id
    #     # Falls partner_id und partner_id.lang und document_template_id vorhanden sind, wird das entsprechende Template mit der Sprache als Parameter ausgewaehlt
    #     if (self.partner_id and self.partner_id.lang and self.document_template_id):
    #         selected_template = self.document_template_id.with_context(lang=self.partner_id.lang)
    #
    #     # Falls ein Template ausgewaehlt wurde, werden header und footer hinzugefuegt
    #     if (selected_template):
    #         self.eq_head_text = selected_template.eq_header
    #         self.comment = selected_template.eq_footer

    @api.model
    def change_template_id(self, quote_template, partner=False, fiscal_position_id=False, order_lines=[]):
        if not quote_template:
            return True

        lines = []  # order_lines

        sale_order_line_obj = self.env['sale.order.line']
        for line in quote_template.eq_quote_line:
            res = sale_order_line_obj.product_id_change()

            # res = sale_order_line_obj.product_id_change(False, line.product_id.id, line.product_uom_qty,
            #                                            line.product_uom_id.id, False, False, line.name,
            #                                            partner, False, False, False, False,
            #                                            fiscal_position_id, False)

            data = res.get('value', {})
            if 'tax_id' in data:
                data['tax_id'] = [(6, 0, data['tax_id'])]
            data.update({
                'name': line.name,
                'price_unit': line.price_unit,
                'discount': line.discount,
                'product_uom_qty': line.product_uom_qty,
                'product_id': line.product_id.id,
                'product_uom': line.product_uom_id.id,
                'website_description': line.website_description,
                'state': 'draft',
            })
            lines.append((0, 0, data))

        return lines

    @api.onchange('document_template_id')
    def onchange_document_template_id(self):
        """
        Übernahme der Texte beim Wechsel des Templates
        :return:
        """
        selected_template = self.document_template_id
        if self.partner_id and self.partner_id.lang and self.document_template_id:
            selected_template = self.document_template_id.with_context(lang=self.partner_id.lang)
        if selected_template:
            self.eq_head_text = selected_template.eq_header
            self.comment = selected_template.eq_footer
            self.pricelist_id = selected_template.eq_pricelist_id

    @api.onchange('partner_id', 'company_id')
    def _onchange_delivery_address(self):
        addr = self.partner_id.address_get(['delivery'])
        self.partner_shipping_id = addr and addr.get('delivery')
        if self.env.context.get('type', 'out_invoice') == 'out_invoice':
            company = self.company_id or self.env.user.company_id
            #self.comment = company.with_context(lang=self.partner_id.lang).sale_note

"""
    def _prepare_invoice(self, cr, uid, order, line_ids, context=None):
        
        invoice_vals = super(eq_report_extension_purchase_order, self)._prepare_invoice(cr, uid, order, line_ids, context)
        
        invoice_vals['document_template_id'] = order.document_template_id.id

        
        return invoice_vals
    
    
    """