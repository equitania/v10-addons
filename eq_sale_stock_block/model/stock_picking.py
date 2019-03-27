# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, _, exceptions
from openerp.models import Model, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare, float_round, float_is_zero
from odoo.exceptions import UserError
import time


class StockPicking(Model):
    _inherit = 'stock.picking'

    blocked = fields.Boolean('Blocked')
    state = fields.Selection([
        ('draft', 'Draft'), ('cancel', 'Cancelled'),
        ('block', 'Blocked'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting Availability'),
        ('partially_available', 'Partially Available'),
        ('assigned', 'Available'), ('done', 'Done')], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=True, store=True, track_visibility='onchange',
        help=" * Draft: not confirmed yet and will not be scheduled until confirmed\n"
             " * Blocked:The related sale order blocks the picking and/or delivery order(needs to be unblocked from related sale order, or via invoice payment)\n"
             " * Waiting Another Operation: waiting for another move to proceed before it becomes automatically available (e.g. in Make-To-Order flows)\n"
             " * Waiting Availability: still waiting for the availability of products\n"
             " * Partially Available: some products are available and reserved\n"
             " * Ready to Transfer: products reserved, simply waiting for confirmation.\n"
             " * Transferred: has been processed, can't be modified or cancelled anymore\n"
             " * Cancelled: has been cancelled, can't be confirmed anymore")

    @api.depends('move_type', 'launch_pack_operations', 'move_lines.state', 'move_lines.picking_id',
                 'move_lines.partially_available','blocked')
    @api.one
    def _compute_state(self):
        ''' State of a picking depends on the state of its related stock.move
         - no moves: draft or assigned (launch_pack_operations)
         - all moves canceled: cancel
         - all moves done (including possible canceled): done
         - All at once picking: least of confirmed / waiting / assigned
         - Partial picking
          - all moves assigned: assigned
          - one of the move is assigned or partially available: partially available
          - otherwise in waiting or confirmed state
        '''
        if not self.move_lines and self.launch_pack_operations:
            self.state = 'assigned'
        elif self.blocked:
            self.state = 'block'
        elif not self.move_lines:
            self.state = 'draft'
        elif any(move.state == 'draft' for move in self.move_lines):  # TDE FIXME: should be all ?
            self.state = 'draft'
        elif all(move.state == 'cancel' for move in self.move_lines):
            self.state = 'cancel'
        elif all(move.state in ['cancel', 'done'] for move in self.move_lines):
            self.state = 'done'
        elif self.move_type == 'one':
            ordered_moves = self.move_lines.filtered(
                lambda move: move.state not in ['cancel', 'done']
            ).sorted(
                key=lambda move: (move.state == 'assigned' and 2) or (move.state == 'waiting' and 1) or 0, reverse=False
            )
            self.state = ordered_moves[0].state
        else:
            filtered_moves = self.move_lines.filtered(lambda move: move.state not in ['cancel', 'done'])
            if not all(move.state == 'assigned' for move in filtered_moves) and any(
                            move.state == 'assigned' for move in filtered_moves):
                self.state = 'partially_available'
            elif any(move.partially_available for move in filtered_moves):
                self.state = 'partially_available'
            else:
                ordered_moves = filtered_moves.sorted(
                    key=lambda move: (move.state == 'assigned' and 2) or (move.state == 'waiting' and 1) or 0,
                    reverse=True)
                self.state = ordered_moves[0].state

    @api.multi
    def action_assign(self):
        """
        Inherit action_assign method so that if the state of the picking is blocked it does not reserve any quantites for the moves
        :return:
        """
        for record in self:
            if not record.state == 'block':
                res = super(StockPicking, self).action_assign()
                return res
            else:
                return

class StockMove(Model):
    _inherit = 'stock.move'

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
                ('state', 'in', ['draft','block','confirmed', 'waiting', 'partially_available', 'assigned'])], limit=1)
            if not picking:
                picking = Picking.create(move._get_new_picking_values())
            move.write({'picking_id': picking.id})
        return True

    _picking_assign = assign_picking
