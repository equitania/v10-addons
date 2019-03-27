# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

class ResPartner(models.Model):

    _inherit = 'res.partner'
    
    @api.onchange('parent_id')
    def _set_parent(self):
        # onchange function which changes the value of customer_number which depends from parent_id
        if self.parent_id:
            if self.parent_id.customer_number:
                self.customer_number = self.parent_id.customer_number
            if self.parent_id.supplier_number:
                self.supplier_number = self.parent_id.supplier_number
