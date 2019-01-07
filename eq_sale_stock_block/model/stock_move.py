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

from openerp import fields, _, exceptions
from openerp.models import Model, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare, float_round, float_is_zero
from odoo.exceptions import UserError
import time


class StockMove(Model):
    _inherit = 'stock.move'

    @api.multi
    def action_done(self):
        """ Process completely the moves given and if all moves are done, it will finish the picking. """

        result = super(StockMove, self).action_done()

        self.filtered(lambda move: move.state == 'draft').action_confirm()

        Uom = self.env['product.uom']
        Quant = self.env['stock.quant']

        pickings = self.env['stock.picking']
        procurements = self.env['procurement.order']
        operations = self.env['stock.pack.operation']

        remaining_move_qty = {}

        for move in self:
            if move.picking_id:
                pickings |= move.picking_id
            remaining_move_qty[move.id] = move.product_qty
            for link in move.linked_move_operation_ids:
                operations |= link.operation_id
                pickings |= link.operation_id.picking_id

        # Sort operations according to entire packages first, then package + lot, package only, lot only
        operations = operations.sorted(
            key=lambda x: ((x.package_id and not x.product_id) and -4 or 0) + (x.package_id and -2 or 0) + (
                x.pack_lot_ids and -1 or 0))

        for operation in operations:

            # product given: result put immediately in the result package (if False: without package)
            # but if pack moved entirely, quants should not be written anything for the destination package
            quant_dest_package_id = operation.product_id and operation.result_package_id.id or False
            entire_pack = not operation.product_id and True or False

            # compute quantities for each lot + check quantities match
            lot_quantities = dict((pack_lot.lot_id.id,
                                   operation.product_uom_id._compute_quantity(pack_lot.qty, operation.product_id.uom_id)
                                   ) for pack_lot in operation.pack_lot_ids)
            if operation.pack_lot_ids and float_compare(sum(lot_quantities.values()), operation.product_qty,
                                                        precision_rounding=operation.product_uom_id.rounding) != 0.0:
                raise UserError(_(
                    'You have a difference between the quantity on the operation and the quantities specified for the lots. '))

            quants_taken = []
            false_quants = []
            lot_move_qty = {}

            prout_move_qty = {}
            for link in operation.linked_move_operation_ids:
                prout_move_qty[link.move_id] = prout_move_qty.get(link.move_id, 0.0) + link.qty

            # Process every move only once for every pack operation
            for move in prout_move_qty.keys():
                # TDE FIXME: do in batch ?
                move.check_tracking(operation)

                # TDE FIXME: I bet the message error is wrong
                if not remaining_move_qty.get(move.id):
                    raise UserError(_(
                        "The roundings of your unit of measure %s on the move vs. %s on the product don't allow to do these operations or you are not transferring the picking at once. ") % (
                                        move.product_uom.name, move.product_id.uom_id.name))

                if not operation.pack_lot_ids:
                    preferred_domain_list = [[('reservation_id', '=', move.id)], [('reservation_id', '=', False)],
                                             ['&', ('reservation_id', '!=', move.id), ('reservation_id', '!=', False)]]
                    quants = Quant.quants_get_preferred_domain(
                        prout_move_qty[move], move, ops=operation, domain=[('qty', '>', 0)],
                        preferred_domain_list=preferred_domain_list)
                    Quant.quants_move(quants, move, operation.location_dest_id, location_from=operation.location_id,
                                      lot_id=False, owner_id=operation.owner_id.id,
                                      src_package_id=operation.package_id.id,
                                      dest_package_id=quant_dest_package_id, entire_pack=entire_pack)
                else:
                    # Check what you can do with reserved quants already
                    qty_on_link = prout_move_qty[move]
                    rounding = operation.product_id.uom_id.rounding
                    for reserved_quant in move.reserved_quant_ids:
                        if (reserved_quant.owner_id.id != operation.owner_id.id) or (
                                    reserved_quant.location_id.id != operation.location_id.id) or \
                                (reserved_quant.package_id.id != operation.package_id.id):
                            continue
                        if not reserved_quant.lot_id:
                            false_quants += [reserved_quant]
                        elif float_compare(lot_quantities.get(reserved_quant.lot_id.id, 0), 0,
                                           precision_rounding=rounding) > 0:
                            if float_compare(lot_quantities[reserved_quant.lot_id.id], reserved_quant.qty,
                                             precision_rounding=rounding) >= 0:
                                lot_quantities[reserved_quant.lot_id.id] -= reserved_quant.qty
                                quants_taken += [(reserved_quant, reserved_quant.qty)]
                                qty_on_link -= reserved_quant.qty
                            else:
                                quants_taken += [(reserved_quant, lot_quantities[reserved_quant.lot_id.id])]
                                lot_quantities[reserved_quant.lot_id.id] = 0
                                qty_on_link -= lot_quantities[reserved_quant.lot_id.id]
                    lot_move_qty[move.id] = qty_on_link

                remaining_move_qty[move.id] -= prout_move_qty[move]

            # Handle lots separately
            if operation.pack_lot_ids:
                # TDE FIXME: fix call to move_quants_by_lot to ease understanding
                self._move_quants_by_lot(operation, lot_quantities, quants_taken, false_quants, lot_move_qty,
                                         quant_dest_package_id)

            # Handle pack in pack
            if not operation.product_id and operation.package_id and operation.result_package_id.id != operation.package_id.parent_id.id:
                operation.package_id.sudo().write({'parent_id': operation.result_package_id.id})

        # Check for remaining qtys and unreserve/check move_dest_id in
        move_dest_ids = set()
        for move in self:
            if float_compare(remaining_move_qty[move.id], 0,
                             precision_rounding=move.product_id.uom_id.rounding) > 0:  # In case no pack operations in picking
                move.check_tracking(False)  # TDE: do in batch ? redone ? check this

                preferred_domain_list = [[('reservation_id', '=', move.id)], [('reservation_id', '=', False)],
                                         ['&', ('reservation_id', '!=', move.id), ('reservation_id', '!=', False)]]
                quants = Quant.quants_get_preferred_domain(
                    remaining_move_qty[move.id], move, domain=[('qty', '>', 0)],
                    preferred_domain_list=preferred_domain_list)
                Quant.quants_move(
                    quants, move, move.location_dest_id,
                    lot_id=move.restrict_lot_id.id, owner_id=move.restrict_partner_id.id)

            # If the move has a destination, add it to the list to reserve
            if move.move_dest_id and move.move_dest_id.state in ('waiting', 'confirmed'):
                move_dest_ids.add(move.move_dest_id.id)

            if move.procurement_id:
                procurements |= move.procurement_id

            # unreserve the quants and make them available for other operations/moves
            move.quants_unreserve()

        # Check the packages have been placed in the correct locations
        self.mapped('quant_ids').filtered(lambda quant: quant.package_id and quant.qty > 0).mapped(
            'package_id')._check_location_constraint()

        # set the move as done
        self.write({'state': 'done', 'date': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        procurements.check()
        # assign destination moves
        if move_dest_ids:
            if self.browse(list(move_dest_ids))[0].picking_id:
                if self.browse(list(move_dest_ids))[0].picking_id.state != 'block':
                    # TDE FIXME: record setise me
                    self.browse(list(move_dest_ids)).action_assign()
        pickings.filtered(lambda picking: picking.state == 'done' and not picking.date_done).write(
            {'date_done': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        return result

    @api.multi
    def assign_picking(self):
        """ Try to assign the moves to an existing picking that has not been
        reserved yet and has the same procurement group, locations and picking
        type (moves should already have them identical). Otherwise, create a new
        picking to assign them to. """
        Picking = self.env['stock.picking']

        # If this method is called in batch by a write on a one2many and
        # at some point had to create a picking, some next iterations could
        # try to find back the created picking. As we look for it by searching
        # on some computed fields, we have to force a recompute, else the
        # record won't be found.
        self.recompute()
        for move in self:
            picking = Picking.search([
                ('group_id', '=', move.group_id.id),
                ('location_id', '=', move.location_id.id),
                ('location_dest_id', '=', move.location_dest_id.id),
                ('picking_type_id', '=', move.picking_type_id.id),
                ('printed', '=', False),
                ('state', 'in', ['draft', 'block', 'confirmed', 'waiting', 'partially_available', 'assigned'])],
                limit=1)
            if not picking:
                picking = Picking.create(move._get_new_picking_values())
            move.write({'picking_id': picking.id})
        return True

    _picking_assign = assign_picking
