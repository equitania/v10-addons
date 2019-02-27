from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    #Validate the vat for the customer
    @api.onchange('partner_id')
    def check_partner_vat(self):
        if self.partner_id and self.partner_id.property_account_position_id and self.partner_id.property_account_position_id.eq_check_vat:
            msg = self.partner_id.eq_check_vat(self.partner_id.vat)
            if msg:
                return {'warning': {'title': _('Invalid VAT'),'message':msg}}

    # Dont Allow the Sale Order to be validated if the customer has invalid VAT number
    @api.multi
    def action_confirm(self):
        order = self
        if order.partner_id.property_account_position_id and order.partner_id.property_account_position_id.eq_check_vat:
            msg = order.partner_id.eq_check_vat(order.partner_id.vat)
            if msg:
                raise ValidationError(msg)
        return super(SaleOrder, self).action_confirm()
