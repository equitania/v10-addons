# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _

"""
Hilfsklassen für die Anzeige von Meldungen in Odoo
"""


class eq_message(models.TransientModel):
    _name = "eq_message"
    
    eq_info = fields.Char("Info")
    eq_message_text = fields.Char("Message")
    
    
class eq_prot_message(models.TransientModel):
    _inherit = ['eq_message']
    
    eq_res_id = fields.Many2one('eq.ebid.protocol', string='Protocol', required=False)
