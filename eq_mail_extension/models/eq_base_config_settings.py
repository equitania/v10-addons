# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api

class EqBaseConfigSettings(models.TransientModel):
    """ EqBaseConfigSettings class inherited from BaseConfigSettings"""
    _inherit = 'base.config.settings'

    @api.model
    def delete_alias_domain(self):
        config_parameters = self.env["ir.config_parameter"]
        config_parameters.set_param("mail.catchall.domain", '')

        return True
