# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api

class EqBaseConfigSettings(models.TransientModel):
    """ EqBaseConfigSettings class inherited from BaseConfigSettings"""
    _inherit = 'base.config.settings'

    @api.model
    def delete_alias_domain(self):
        config_parameters = self.env["ir.config_parameter"]
        config_parameters.set_param("mail.catchall.domain", '')

        return True
