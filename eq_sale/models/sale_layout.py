# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class SaleLayoutCategory(models.Model):
    # _name = 'sale_layout.category'
    _inherit = 'sale.layout_category'
    _order = 'sequence'

    separator = fields.Boolean('Add separator', default=True)


# auskommentiert da bereits im Standard vorhanden
# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#
#     """
#     sale_layout_cat_id = fields.Many2one('sale_layout.category',
#                                               string='Section')
#
#     categ_sequence = fields.Integer(related='sale_layout_cat_id.sequence', string='Layout Sequence', store=True)
#
#         #  Store is intentionally set in order to keep the "historic" order.
#
#
#     _defaults = {
#         'categ_sequence': 0
#     }
#     """ # auskommentiert da bereits im Standard vorhanden
#
#     _order = 'order_id, sequence, id'  # categ_sequence = layout_category_sequence in Basis; sale_layout_cat_id = layout_category_id in Basis
#
#     # Übernahme der Sektion bereits im Standard
#     # def _prepare_order_line_invoice_line(self, line, account_id=False, context=None):
#     #     """Save the layout when converting to an invoice line."""
#     #     invoice_vals = super(SaleOrderLine, self)._prepare_order_line_invoice_line(cr, uid, line, account_id=account_id, context=context)
#     #     if line.layout_category_id:
#     #         invoice_vals['layout_category_id'] = line.layout_category_id.id
#     #     if line.layout_category_sequence:
#     #         invoice_vals['layout_category_sequence'] = line.layout_category_sequence
#     #     return invoice_vals
