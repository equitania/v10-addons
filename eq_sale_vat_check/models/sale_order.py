# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    #Validate the vat for the customer
    @api.onchange('partner_shipping_id')
    def check_partner_vat(self):
        if self.partner_shipping_id and self.partner_shipping_id.property_account_position_id and self.partner_shipping_id.property_account_position_id.eq_check_vat:
            msg = self.partner_shipping_id.eq_check_vat(self.partner_shipping_id.vat)
            if msg:
                return {'warning': {'title': _('Invalid VAT'),'message':msg}}

    # Dont Allow the Sale Order to be validated if the customer has invalid VAT number
    @api.multi
    def action_confirm(self):
        order = self
        if order.partner_shipping_id.property_account_position_id and order.partner_shipping_id.property_account_position_id.eq_check_vat:
            msg = order.partner_shipping_id.eq_check_vat(order.partner_shipping_id.vat)
            if msg:
                raise ValidationError(msg)
        return super(SaleOrder, self).action_confirm()
