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


from odoo import models, fields, api, _

class res_partner(models.Model):
    _inherit = 'res.partner'

    def _sale_quotation_count(self):
        # The current user may not have access rights for sale orders
        for partner in self:
            partner.eq_sale_quotation_count = len(partner.sale_order_ids.filtered(lambda record: record.state in ('draft', 'sent', 'cancel'))) + len(partner.mapped('child_ids.sale_order_ids').filtered(lambda record: record.state in ('draft', 'sent', 'cancel')))
            partner.sale_order_count = len(partner.sale_order_ids.filtered(lambda record: record.state not in ('draft', 'sent', 'cancel'))) + len(partner.mapped('child_ids.sale_order_ids').filtered(lambda record: record.state not in ('draft', 'sent', 'cancel')))

    def default_user_id(self):
        user_id = False
        ir_values_obj = self.env['ir.values']
        creator = ir_values_obj.get_default('res.partner', 'default_creator_saleperson')
        if creator:
            user_id = self._uid
        return user_id

    user_id = fields.Many2one('res.users', string='Salesperson',
      help='The internal user that is in charge of communicating with this contact if any.', default=default_user_id)


    eq_sale_quotation_count = fields.Integer(compute="_sale_quotation_count", string='# of Quotations')
    sale_order_count = fields.Integer(compute="_sale_quotation_count", string='# of Orders')
    eq_delivery_condition_id = fields.Many2one('eq.delivery.conditions', 'Delivery Condition')


class eq_partner_extension_base_config_settings(models.TransientModel):
    _inherit = "sale.config.settings"

    def set_default_creator(self):
        ir_values_obj = self.env['ir.values']
        ir_values_obj.set_default('res.partner', 'default_creator_saleperson', self.default_creator_saleperson or False)

    def get_default_creator(self, fields):
        ir_values_obj = self.env['ir.values']
        creator = ir_values_obj.get_default('res.partner', 'default_creator_saleperson')
        return {
            'default_creator_saleperson': creator,
        }

    # def set_default_reset_password(self, cr, uid, ids, context):
    #     ir_values_obj = self.pool.get('ir.values')
    #     config = self.browse(cr, uid, ids[0], context)
    #
    #     ir_values_obj.set_default(cr, uid, 'res.users', 'default_reset_passwort',
    #                               config.default_reset_passwort or False)
    #
    # def get_default_reset_password(self, cr, uid, ids, context):
    #     ir_values_obj = self.pool.get('ir.values')
    #     reset = ir_values_obj.get_default(cr, uid, 'res.users', 'default_reset_passwort')
    #     return {
    #         'default_reset_passwort': reset,
    #     }

    default_creator_saleperson = fields.Boolean('The creator of the address dataset will be set automatically as sales person. [equitania]')
    # 'default_reset_passwort': fields.boolean('Send a reset-password email, if a new user will created. [equitania]')

