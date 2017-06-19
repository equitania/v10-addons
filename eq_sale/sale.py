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



class eq_partner_sale_order_extension(models.Model):
    _inherit = 'sale.order'


    eq_delivery_condition_id = fields.Many2one('eq.delivery.conditions', 'Delivery Condition')
        # 'partner_id': fields.many2one('res.partner', 'Customer', readonly=True,
        #                               states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        #                               required=True, change_default=True, select=True, track_visibility='always'),



    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """
        Override für Wechsel der Partner_ID: Übernahme der custom-Felder
        Umfang noch abzuklären (eq_incoterm; VEP-25)
        :return:
        """

        super(eq_partner_sale_order_extension, self).onchange_partner_id()

        partner = self.partner_id
        if partner:
            # if partner.eq_incoterm:
            #     self.incoterm = partner.eq_incoterm.id
            # else:
            #     self.incoterm = False

            if partner.eq_delivery_condition_id:
                self.eq_delivery_condition_id = partner.eq_delivery_condition_id.id
            else:
                self.eq_delivery_condition_id = False

            self.client_order_ref = partner.eq_foreign_ref

            # if partner.eq_default_delivery_address:
            #     self.partner_shipping_id = partner.eq_default_delivery_address.id
            # if partner.eq_default_invoice_address:
            #     self.partner_invoice_id = partner.eq_default_invoice_address.id

