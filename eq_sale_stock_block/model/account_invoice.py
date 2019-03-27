# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from openerp.models import Model
from openerp import api, fields, SUPERUSER_ID, exceptions

LOG = logging.getLogger(__name__)


class AccountInvoice(Model):
    _inherit = 'account.invoice'

    @api.multi
    def write(self, vals):
        res = super(AccountInvoice, self).write(vals)
        if vals.get('state', False):
            if vals['state'] == 'paid':
                for invoice in self:
                    if invoice.state == 'paid':
                        sale_order = invoice.mapped('invoice_line_ids.sale_line_ids.order_id')[:1]
                        if sale_order:
                            if sale_order.picking_blocked:
                                sale_order.unblock_pickings()
                            if sale_order.delivery_blocked:
                                sale_order.unblock_delivery()
        return res
