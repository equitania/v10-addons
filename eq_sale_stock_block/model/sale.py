# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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
