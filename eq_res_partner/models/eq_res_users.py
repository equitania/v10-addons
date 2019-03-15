# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class eq_res_users(models.Model):
    _inherit = 'res.users'
    # _rec_name = 'display_name'

    eq_firstname = fields.Char(related='partner_id.eq_firstname', inherited=True)

    @api.depends('eq_firstname', 'name')
    def _compute_full_display_name(self):
        """
        Display the full name (eq_firstname + name), or display only the name
        """
        names = dict(self.name_get())
        for record in self:
            record.display_name = names.get(record.id, False)

    @api.multi
    def _search_display_name(self, operator, operand):
        """
        Function which is executed on search by display_name field.
        """
        if operator in ['=', 'ilike']:
            users = self.env['res.users'].search([]).filtered(
                lambda x: operand in x.display_name)
            if users:
                return [('id', 'in', [x.id for x in users])]
            else:
                return [('id', '=', False)]

    display_name = fields.Char(compute='_compute_full_display_name', string='Name', search='_search_display_name')

    def name_get(self):
        """
        For showing both eq_firstname and name in the dropdown of many2one field
        :return: if eq_firstname full name, else name
        """
        res = []
        for user in self:
            if user:
                name = ''
                if user.eq_firstname:
                    name = user.eq_firstname
                if user.name:
                    name = name + ' ' + user.name
                res.append((user.id, name))
        return res

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """
        Added searching for eq_firstname and display_name
        """
        if args is None:
            args = []
        users = self.browse()
        if name and operator in ['=', 'ilike']:
            users = self.search([('login', '=', name)] + args, limit=limit)
        if not users:
            users = self.search(['|','|',('display_name', operator, name),('name', operator, name),('eq_firstname', operator, name)] + args, limit=limit)
        return users.name_get()
