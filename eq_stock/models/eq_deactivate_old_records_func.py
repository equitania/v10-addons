# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class eq_deactivate_old_records_func(models.Model):
    """
    Simple helper class that will be executed during each update of this module
    """
    _name = "eq_deactivate_old_records_func"

    def _deactivate_old_records(self):
        """
        Deactivate old records - we don't need them anymore
        """
        record_ids = self.env['stock.incoterms'].search([])
        old_record_names = [
            "EX WORKS", "FREE CARRIER", "FREE ALONGSIDE SHIP", "FREE ON BOARD", "COST AND FREIGHT", "COST, INSURANCE AND FREIGHT", "CARRIAGE PAID TO",
            "CARRIAGE AND INSURANCE PAID TO", "DELIVERED AT FRONTIER", "DELIVERED EX SHIP", "DELIVERED EX QUAY", "DELIVERED DUTY UNPAID",
            "DELIVERED AT TERMINAL", "DELIVERED AT PLACE", "DELIVERED DUTY PAID"
        ]
        for record in record_ids:
            if record.name in old_record_names:
                record.active = False
