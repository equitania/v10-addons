# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class eq_purchase_order_line(models.Model):
    _inherit = 'purchase.order.line'

    def _generate_default_tax(self):
        ir_values_obj = self.env['ir.values']
        account_tax_id = ir_values_obj.get_default('purchase.order', 'eq_default_tax_purchase_order')
        account_tax_obj = self.browse(account_tax_id)

        if len(account_tax_obj) > 0:
            tax_obj = account_tax_obj[0]
            return tax_obj
        else:
            pass

    taxes_id = fields.Many2many('account.tax', string='Taxes',domain=['|', ('active', '=', False), ('active', '=', True)], default = _generate_default_tax)
    product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True)],
                                 change_default=True, required=False)


class eq_purchase_configuration_address(models.TransientModel):
    _inherit = 'purchase.config.settings'

    def set_default_values(self):
        ir_values_obj = self.env['ir.values']

        ir_values_obj.set_default('purchase.order', 'eq_default_tax_purchase_order', self.eq_default_tax_purchase_order.id or False)

    def get_default_values(self, fields):
        ir_values_obj = self.env['ir.values']
        default_tax_purchase_order = ir_values_obj.get_default('purchase.order', 'eq_default_tax_purchase_order')

        return {
            'eq_default_tax_purchase_order': default_tax_purchase_order,
        }

    eq_default_tax_purchase_order = fields.Many2one('account.tax',string='Free position default tax in po [eq_purchase_free_positions]',
                                           default_model='purchase.order', domain = "[('type_tax_use', '=', 'purchase')]")
