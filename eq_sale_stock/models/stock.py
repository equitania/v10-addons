# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

class eq_stock_picking_extension(models.Model):
    _inherit = 'stock.picking'

    @api.depends('move_lines')
    def _compute_sale_order_id(self):
        for picking in self:
            ref = picking.group_id.name
            sale_order_obj = self.env['sale.order']
            sale_order_ids = sale_order_obj.search([("name", "=", ref)])
            if sale_order_ids and len(sale_order_ids) > 0:
                found_sale_order = sale_order_ids[0]
                picking.eq_sale_order_id = found_sale_order.id

    def eq_drop_eq_sale_order_id(self):
        ir_module_obj = self.env['ir.module.module'].search([('name', '=', 'eq_sale_stock'),('write_date','<','2018-12-20 14:00:00')])
        if len(ir_module_obj) > 0:
            self._cr.execute('alter table stock_picking drop column eq_sale_order_id cascade')

    eq_sale_order_id = fields.Many2one('sale.order', 'SaleOrder', compute='_compute_sale_order_id', store=True)
    # eq_header_text = fields.Html(string="Header")
    # eq_footer_text = fields.Html(string="Footer")

    @api.model
    def create(self, vals):
        """
            Extended version of create method. We're using this in process "Confirm an order" to be able to set link between sale order and stock_picking.
            It's a simple solution to save sale_order_id defined as many2one field eq_sale_order_id.
            @vals: values to be saved
            @return: defaul result
        """
        sale_order_obj = self.env['sale.order']
        sale_order_ids = sale_order_obj.search([("name", "=", vals["origin"])])  # let's find linked sale_order to be able to save it's ID in our field
        if sale_order_ids and len(sale_order_ids) > 0:
            found_sale_order = sale_order_ids[0]
            #vals['eq_sale_order_id'] = found_sale_order.id  # ok, we've got it...save it
            vals['eq_header_text'] = found_sale_order.eq_head_text
            vals['eq_footer_text'] = found_sale_order.note

        return super(eq_stock_picking_extension, self).create(vals)

    def _prepare_pack_ops(self, quants, forced_qties):
        """Added eq_description to pack_op_vals"""
        self.ensure_one()
        res = super(eq_stock_picking_extension, self)._prepare_pack_ops(
            quants, forced_qties,
        )

        # Create dictionary with key product_id and value description(name) from the corresponding move,
        # after that put it in pack_op_vals depending on the product_id
        product_description = dict()
        picking_moves = self.move_lines.filtered(lambda move: move.state not in ('done', 'cancel'))
        for move in picking_moves:
            if move.name:
                if move.product_id.id in product_description and product_description[move.product_id.id]:
                    product_description[move.product_id.id] = product_description[move.product_id.id] + " " \
                                                              + (move.name).strip()
                else:
                    product_description[move.product_id.id] = move.name

        for pack_op_vals in res:
            if 'product_id' in pack_op_vals:
                pack_op_vals['eq_description'] = product_description[pack_op_vals['product_id']]

        return res