# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, _
from datetime import datetime
from odoo.exceptions import UserError, AccessError

class EqPurchaseOrder(models.Model):
    _inherit = "purchase.order"
        
    @api.multi
    def _create_picking(self):
        """
        Override _create_picking function which allow separete picking creation
        """
        StockPicking = self.env['stock.picking']
        for order in self:
            if any([ptype in ['product', 'consu'] for ptype in order.order_line.mapped('product_id.type')]):
                moves = []
                # For every purchase line which have different date_planned create new picking, 
                # if picking with same date exist, set existing
                for order_line_id in order.order_line:
                    pickings = order.picking_ids.filtered(lambda x: x.state not in ('done','cancel'))
                    if pickings:
                        for rec in pickings:
                            min_date = datetime.strptime(rec.min_date, '%Y-%m-%d %H:%M:%S').date()
                            date_planned = datetime.strptime(order_line_id.date_planned, '%Y-%m-%d %H:%M:%S').date()
                            if min_date == date_planned:
                                pickings = True
                                picking = rec
                                break
                            pickings = False
                    if not pickings:
                        res = order_line_id._prepare_picking()
                        picking = StockPicking.create(res)
                        
                    moves_obj = order_line_id._create_stock_moves(picking)
                    for move_obj in moves_obj:
                        moves.append(move_obj.id)
                moves = self.env['stock.move'].browse(moves)
                moves = moves.filtered(lambda x: x.state not in ('done', 'cancel')).action_confirm()
                seq = 0
                for move in sorted(moves, key=lambda move: move.date_expected):
                    seq += 5
                    move.sequence = seq
                moves.force_assign()
                pickings = order.picking_ids.filtered(lambda x: x.state not in ('done','cancel'))
                for picking in pickings:
                    picking.message_post_with_view('mail.message_origin_link',
                        values={'self': picking, 'origin': order},
                        subtype_id=self.env.ref('mail.mt_note').id)
        return True
        
class EqPurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
    
    @api.model
    def _prepare_picking(self):
        """
        New function - to allow picking preparation for purchase lines with different date_planned
        """
        if not self.order_id.group_id:
            self.order_id.group_id = self.order_id.group_id.create({
                'name': self.order_id.name,
                'partner_id': self.order_id.partner_id.id
            })
        if not self.order_id.partner_id.property_stock_supplier.id:
            raise UserError(_("You must set a Vendor Location for this partner %s") % self.partner_id.name)
        return {
            'picking_type_id': self.order_id.picking_type_id.id,
            'partner_id': self.order_id.partner_id.id,
            'date': self.date_planned,
            'origin': self.order_id.name,
            'location_dest_id': self.order_id._get_destination_location(),
            'location_id': self.order_id.partner_id.property_stock_supplier.id,
            'company_id': self.order_id.company_id.id,
        }
