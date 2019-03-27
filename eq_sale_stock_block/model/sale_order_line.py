# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from openerp.models import Model, api


_logger = logging.getLogger(__name__)


class SaleOrderLine(Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _action_procurement_create(self):
        res = super(SaleOrderLine, self)._action_procurement_create()
        orders = list(set(x.order_id for x in self))
        for order in orders:
            if order.picking_blocked:
                blocked_picking = order.picking_ids.filtered(lambda x: x.picking_type_id.picking_type == 'pick')
                if blocked_picking:
                    blocked_picking.do_unreserve()
                    blocked_picking.write({'blocked':True,'state': 'block'})
            if order.delivery_blocked:
                blocked_delivery = order.picking_ids.filtered(lambda x: x.picking_type_id.picking_type == 'pack')
                if blocked_delivery:
                    blocked_delivery.do_unreserve()
                    blocked_delivery.write({'blocked':True,'state': 'block'})
        return res
