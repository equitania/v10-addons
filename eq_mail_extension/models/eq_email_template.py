# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields

class EqMailTemplate(models.Model):
    """ EqMailTemplate class inhertied from MailTemplate"""
    _inherit = 'mail.template'

    eq_email_template_version = fields.Integer(string="Version Number")
