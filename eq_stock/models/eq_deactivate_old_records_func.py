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
