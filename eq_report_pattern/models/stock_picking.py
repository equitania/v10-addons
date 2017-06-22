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



class eq_stock_picking(models.Model):
    _inherit = 'stock.picking'
   
    document_template_id = fields.Many2one(comodel_name='eq.document.template', string='Document Template')#TODO: readonly falls Rechnung nicht mehr editierbar?
    # eq_header_text = fields.Html(string="Header")
    # eq_footer_text = fields.Html(string="Footer")
    
    # account.invoice enthaelt die selbe Methode und ist auf die selbe Art ueberschrieben
    @api.onchange('document_template_id')
    def onchange_document_template_id(self):
        selected_template = self.document_template_id
        if (self.partner_id and self.partner_id.lang and self.document_template_id):
            selected_template = self.document_template_id.with_context(lang=self.partner_id.lang)
            
        if (selected_template):
            self.eq_header_text = selected_template.eq_header
            self.eq_footer_text = selected_template.eq_footer
            
    # Automatsichen Test anlegen
    # Erzeugt einen Pickingauftrag?
    # War deprecated, muss getestet werden.[funktioniert]
    @api.model
    def create(self, vals):
        sale_order_obj = self.env['sale.order']
        sale_order_ids = sale_order_obj.search([("name", "=", vals["origin"])])
        if sale_order_ids:
            sale_order_origin = sale_order_ids[0]
            if sale_order_origin:
                vals['eq_header_text'] = sale_order_origin.eq_head_text
                vals['eq_footer_text'] = sale_order_origin.note
                vals['document_template_id'] = sale_order_origin.document_template_id.id
        
        return super(eq_stock_picking, self).create(vals)