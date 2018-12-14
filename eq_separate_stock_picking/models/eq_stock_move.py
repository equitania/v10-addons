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

from odoo import api, models, fields, _
from datetime import datetime

class EqStockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    def assign_picking(self):
        # Overrided base assign_picking function
        """ Try to assign the moves to an existing picking that has not been
        reserved yet and has the same procurement group, locations and picking
        type (moves should already have them identical). Otherwise, create a new
        picking to assign them to. """
        Picking = self.env['stock.picking']
        for move in self:
            recompute = False
            
            picking = Picking.search([
                ('group_id', '=', move.group_id.id),
                ('location_id', '=', move.location_id.id),
                ('location_dest_id', '=', move.location_dest_id.id),
                ('picking_type_id', '=', move.picking_type_id.id),
                ('printed', '=', False),
                ('state', 'in', ['draft', 'confirmed', 'waiting', 'partially_available', 'assigned'])])
            
            if picking:
                # It is necessary because min date is 'datetime' and eq delivery date is 'date'
                for rec in picking:
                    min_date = datetime.strptime(rec.min_date, '%Y-%m-%d %H:%M:%S').date()
                    eq_delivery_date = datetime.strptime(move.sale_line_id.eq_delivery_date, '%Y-%m-%d').date()
                    if min_date == eq_delivery_date:
                        picking = rec
                        break
                    picking = False
                    
            if not picking:
                recompute = True
                picking = Picking.create(move._get_new_picking_values())
                    
            move.write({'picking_id': picking.id})

            # If this method is called in batch by a write on a one2many and
            # at some point had to create a picking, some next iterations could
            # try to find back the created picking. As we look for it by searching
            # on some computed fields, we have to force a recompute, else the
            # record won't be found.
            if recompute:
                move.recompute()
            
            # With this part, message for the origin of the transfer is created on Delivery Order
            if move.picking_id and move.picking_id.group_id:
                picking = move.picking_id
                order = self.env['sale.order'].sudo().search([('procurement_group_id', '=', picking.group_id.id)])
                picking.message_post_with_view(
                    'mail.message_origin_link',
                    values={'self': picking, 'origin': order},
                    subtype_id=self.env.ref('mail.mt_note').id)
        return True
    
    def _get_new_picking_values(self):
        # Overrided base _get_new_picking_values function
        """ Prepares a new picking for this move as it could not be assigned to
        another picking. This method is designed to be inherited. """
        
        # Added min_date, set from eq_delivery_date of the corresponding sale_line_id
        return {
            'origin': self.origin,
            'company_id': self.company_id.id,
            'move_type': self.group_id and self.group_id.move_type or 'direct',
            'partner_id': self.partner_id.id,
            'picking_type_id': self.picking_type_id.id,
            'location_id': self.location_id.id,
            'location_dest_id': self.location_dest_id.id,
            'min_date': self.sale_line_id.eq_delivery_date
        }