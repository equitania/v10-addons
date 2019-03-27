# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from openerp.models import Model
from openerp import api, fields, SUPERUSER_ID

LOG = logging.getLogger(__name__)


class AccountPaymentTerm(Model):
    _inherit = 'account.payment.term'

    block_picking = fields.Boolean('Block Picking')
    block_delivery = fields.Boolean('Block Delivery')
