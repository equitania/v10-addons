# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields

class EqMailTemplate(models.Model):
    """ EqMailTemplate class inhertied from MailTemplate"""
    _inherit = 'mail.template'

    eq_email_template_version = fields.Integer(string="Version Number")
