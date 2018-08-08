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

import logging
from openerp import fields
from openerp.models import Model, _, api

_logger = logging.getLogger(__name__)


class SaleOrder(Model):
    _inherit = "sale.order"

    picking_blocked = fields.Boolean('Picking Blocked')
    delivery_blocked = fields.Boolean('Delivery Blocked')

    @api.model
    def create(self, values):
        """
        Override the create method so if the related payment_term_id is block_purchase the created order is also
        block_purchase.
        :param values:
        :return: record
        """
        order = super(SaleOrder, self).create(values)
        if order.payment_term_id.block_picking:
            order.write({'picking_blocked': True})
        if order.payment_term_id.block_delivery:
            order.write({'delivery_blocked': True})
        return order

    @api.multi
    def write(self, values):
        """
        Override the write method so each time the payment term is updated the purchase block is changed accordingly
        :param values:
        :return:
        """
        res = super(SaleOrder, self).write(values)
        for record in self:
            if 'payment_term_id' in values:
                if values['payment_term_id']:
                    record.update({'picking_blocked': record.payment_term_id.block_picking,
                                   'delivery_blocked': record.payment_term_id.block_delivery})
                else:
                    record.update({'picking_blocked': False, 'delivery_blocked': False})
        return res

    @api.multi
    def unblock_pickings(self):
        """
        Unblock all related pickings that are in state blocked and that are of type internal
        :return:
        """
        for order in self:
            if order.picking_blocked:
                blocked_picking = order.picking_ids.filtered(
                    lambda x: x.state == 'block' and x.picking_type_id.picking_type == 'pick')
                if blocked_picking:
                    order.write({'picking_blocked': False})
                    blocked_picking.write({'blocked':False,'state': 'confirmed'})
                    blocked_picking.action_assign()

    @api.multi
    def unblock_delivery(self):
        """
        Unblock all related pickings that are in stage block anf that are of type outgoing
        :return:
        """
        for order in self:
            if order.delivery_blocked:
                order.unblock_pickings()
                blocked_delivery = order.picking_ids.filtered(
                    lambda x: x.state == 'block' and x.picking_type_id.picking_type == 'pack')
                if blocked_delivery:
                    order.write({'delivery_blocked': False})
                    blocked_delivery.write({'blocked':False,'state': 'confirmed'})
                    blocked_delivery.action_assign()
