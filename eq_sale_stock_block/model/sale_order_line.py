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

    #