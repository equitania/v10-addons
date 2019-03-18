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
from odoo.exceptions import ValidationError

# Erzeugt neue Dokumentvorlage die einen header, footer und den Inhalt enthaelt
class eq_document_template(models.Model):
    _name = "eq.document.template"
    
    name = fields.Char(string="Name", translate=True, required=True)
    eq_model = fields.Selection(selection=[('sale.order', 'Sale Order'), ('purchase.order', 'Purchase Order'),('account.invoice',"Invoice"),('stock.picking',"Delivery")],string="Model")
    eq_quote_line = fields.One2many('eq.sale.quote.line', 'quote_id', 'Quote Template Lines', copy=True)
    eq_header = fields.Html(string="Header", translate=True)
    eq_footer = fields.Html(string="Footer", translate=True)
    eq_default = fields.Boolean(string="Default value")
    eq_pricelist_id = fields.Many2one(string="Pricelist",comodel_name="product.pricelist")


    # Check if there is already a default value
    @api.constrains('eq_default')
    def get_default(self):
        eq_default = self.search([("eq_model","=",self.eq_model),('eq_default','=',True),("id","!=",self.id)],limit=1)
        if eq_default and self.eq_default:
            raise ValidationError(_('Current default template for %s is %s,you can not have more than one.')%(dict(eq_default._fields['eq_model'].selection).get(eq_default.eq_model),eq_default.name))

    