# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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

    