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


class eq_res_users(models.Model):
    _inherit = 'res.users'
    # _rec_name = 'display_name'

    eq_firstname = fields.Char(related='partner_id.eq_firstname', inherited=True)

    def _compute_full_display_name(self):
        # Display the full name (eq_firstname + name), or display only the name

        for user in self:
            if user.eq_firstname and user.name:
                user.display_name = user.eq_firstname + ' ' + user.name
            else:
                user.display_name = user.name

    display_name = fields.Char(compute='_compute_full_display_name', string='Name')

    def name_get(self):
        """
        For showing both eq_firstname and name in the dropdown of many2one field
        :return: if eq_firstname full name, else name
        """
        res = []

        for user in self:
            if user.eq_firstname and user.name:
                res.append((user.id, user.eq_firstname + ' ' + user.name))
            else:
                res.append((user.id, user.name))

        return res