# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields

class EqLetter(models.Model):
    """
    Class EqLetter
    """
    _name = 'eq_letter'
    _rec_name = 'eq_letter_subject'

    eq_text = fields.Html('Text', required=True)

    def get_current_user(self):
        """
        Default function which return value for eq_letter_form field
        :return: partner id
        """
        obj = self.env['res.users'].search([('id', '=', self._uid)])
        return obj.partner_id

    eq_letter_from = fields.Many2one(
        'res.partner', string='From', default=get_current_user, required=True)
    eq_letter_subject = fields.Char('Subject', required=False)
    eq_letter_to = fields.Many2one('res.partner', string="To", required=True)
