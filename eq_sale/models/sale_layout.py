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
