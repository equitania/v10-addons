# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, _, exceptions
from openerp.models import Model, api



class StockPicking(Model):
    _inherit = 'stock.picking.type'

    picking_type = fields.Selection([('pick','Pick'),('pack','Pack/Delivery')],string='Picking Type')
