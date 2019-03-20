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

class eq_purchase_order_template(models.Model):
    _inherit = 'purchase.order'

    # Get default template
    def _get_default_template(self):
        eq_default = self.env["eq.document.template"].search([("eq_model", "=", "purchase.order"), ('eq_default', '=', True)],limit=1)
        if eq_default:
            return eq_default
   
    document_template_id = fields.Many2one(comodel_name='eq.document.template', string='Document Template', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},domain="['|',('eq_model', '=', False),('eq_model','=','purchase.order')]}",default=_get_default_template)

    @api.model
    def change_purchase_template_id(self, quote_template):
        lines = []  # order_lines
        for line in quote_template.eq_quote_line:
            data={}
            taxes = line.product_id.supplier_taxes_id
            fpos = self.fiscal_position_id
            taxes_id = fpos.map_tax(taxes) if fpos else taxes
            if taxes_id:
                taxes_id = taxes_id.filtered(lambda x: x.company_id.id == self.company_id.id)
            data.update({
                'name': line.name,
                'price_unit': line.price_unit,
                'discount': line.discount,
                'product_qty': line.product_uom_qty,
                'product_id': line.product_id.id,
                'product_uom': line.product_uom_id.id,
                'website_description': line.website_description,
                'state': 'draft',
                'date_planned':datetime.datetime.now(),
                'taxes_id':[[6,0,taxes_id.ids]]
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
            if self.document_template_id:
                res = self.change_purchase_template_id(selected_template)
                if res:
                    for order_line in self.order_line:
                        res.append((4, order_line.id))
                    self.order_line = res

        self.eq_head_text = selected_template.eq_header
        self.notes = selected_template.eq_footer
    