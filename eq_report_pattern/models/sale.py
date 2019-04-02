# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
import datetime
import time
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

class eq_sale_order_template(models.Model):
    _inherit = 'sale.order'

    # Get default template
    def _get_default_template(self):
        eq_default = self.env["eq.document.template"].search(
            [("eq_model", "=", "sale.order"), ('eq_default', '=', True)], limit=1)
        if eq_default:
            return eq_default
   
    document_template_id = fields.Many2one(comodel_name='eq.document.template', string='Document Template',domain="['|',('eq_model', '=', False),('eq_model','=','sale.order')]}",default=_get_default_template)

    # Automatischen Test anlegen
    @api.model
    def change_template_id(self, quote_template, partner=False, fiscal_position_id=False, order_lines=[]):
        if not quote_template:
            return True

        lines = []  # order_lines

        sale_order_line_obj = self.env['sale.order.line']
        for line in quote_template.eq_quote_line:
            # res = line.product_id_change()

            #res = sale_order_line_obj.product_id_change(False, line.product_id.id, line.product_uom_qty,
            #                                            line.product_uom_id.id, False, False, line.name,
            #                                            partner, False, False, False, False,
            #                                            fiscal_position_id, False)

            data = {}
            # aus _compute_tax_id in Basis übernommen
            try:
                fpos = self.fiscal_position_id or self.partner_id.property_account_position_id
                # If company_id is set, always filter taxes by the company
                taxes = line.product_id.taxes_id.filtered(lambda r: not self.company_id or r.company_id == self.company_id)
                data['tax_id'] = fpos.map_tax(taxes, line.product_id, line.order_id.partner_shipping_id) if fpos else taxes
            except:
                pass

            data.update({
                'name': line.name,
                'price_unit': line.price_unit,
                'discount': line.discount,
                'product_uom_qty': line.product_uom_qty,
                'product_id': line.product_id.id,
                'product_uom': line.product_uom_id.id,
                'website_description': line.website_description,
                'state': 'draft',
                'layout_category_id': line.layout_category_id
            })
            lines.append((0, 0, data))

        return lines

    @api.onchange('document_template_id')
    def onchange_document_template_id(self):
        selected_template = self.document_template_id
        if self.partner_id and self.partner_id.lang and self.document_template_id:
            selected_template = self.document_template_id.with_context(lang=self.partner_id.lang)
        if selected_template:
            self.eq_head_text = selected_template.eq_header
            self.note = selected_template.eq_footer
            partner_id = False
            if self.partner_id:
                partner_id = self.partner_id.id
            if self.state == "draft":
                self.pricelist_id = selected_template.eq_pricelist_id
                res = self.change_template_id(selected_template, partner_id, self.fiscal_position_id,self.order_line)
                if res:
                    for sale_order_line in self.order_line:
                        res.append((4,sale_order_line.id))
                    self.order_line = res


    # Automatischen Test anlegen
    # War deprecated, muss getestet werden.
    @api.multi
    def _prepare_invoice(self):
        """
        Überschrieben zum Setzen der Dokumentenvorlage
        :return:
        """
        result = super(eq_sale_order_template, self)._prepare_invoice()
        # if self.event_id:
            # result['eq_head_text'] = order.eq_head_text
            # result['comment'] = order.note
        
        if self.document_template_id:
            result['document_template_id'] = self.document_template_id.id
          
        return result