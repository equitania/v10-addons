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
