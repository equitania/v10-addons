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



from openerp import models, fields, api, _
import datetime
import time
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

class eq_purchase_order_template(models.Model):
    _inherit = 'purchase.order'
   
    document_template_id = fields.Many2one(comodel_name='eq.document.template', string='Document Template', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})

    
    # @api.onchange('document_template_id')
    # def onchange_document_template_id(self):
    #     selected_template = self.document_template_id
    #     if (self.partner_id and self.partner_id.lang and self.document_template_id):
    #         selected_template = self.document_template_id.with_context(lang=self.partner_id.lang)
    #
    #     if (selected_template):
    #         self.eq_head_text = selected_template.eq_header
    #         self.notes = selected_template.eq_footer

    @api.model
    def change_template_id(self, quote_template, partner=False, fiscal_position_id=False, order_lines=[]):
        if not quote_template:
            return True

        lines = []  # order_lines

        sale_order_line_obj = self.env['sale.order.line']
        for line in quote_template.eq_quote_line:
            res = sale_order_line_obj.product_id_change()

            #res = sale_order_line_obj.product_id_change(False, line.product_id.id, line.product_uom_qty,
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

        selected_template = self.document_template_id
        if (self.partner_id and self.partner_id.lang and self.document_template_id):
            selected_template = self.document_template_id.with_context(lang=self.partner_id.lang)

        if (selected_template):
            self.eq_head_text = selected_template.eq_header
            self.note = selected_template.eq_footer
            partner_id = False
            if (self.partner_id):
                partner_id = self.partner_id.id
            if (self.document_template_id):
                res = self.change_template_id(selected_template, partner_id, self.fiscal_position_id,
                                              self.order_line)
                # if (res and 'value' in res and 'order_line' in res['value'] and res['value']['order_line']):
                if (res):
                    self.order_line = res

        self.eq_head_text = selected_template.eq_header
        self.notes = selected_template.eq_footer
    