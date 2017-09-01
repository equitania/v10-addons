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


class eq_hr_employee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def create(self, values):
        """
        Neuanlage eines Mitarbeiters
        Gewählter Benutzer darf nur diesem Mitarbeiter zugewiesen sein und kein anderer Benutzer darf auf diesen Mitarbeiter verweisen
        :param values:
        :return:
        """

        context_new = {}
        if self._context:
            context_new = dict(self._context)
        context_new['do_not_repeat'] = True

        res = super(eq_hr_employee, self).create(values)
        if 'user_id' in values and 'do_not_repeat' not in self._context:
            if values['user_id']:
                user_obj = self.env['res.users']
                cur_user = user_obj.browse(values['user_id'])

                # Für andere Mitarbeiter den verknüpften Benutzer zurücksetzen, falls dieser dem aktuellen Benutzer entspricht
                emp_ids_to_del = self.search([('user_id', '=', values['user_id']), ('id', '!=', res.id)])
                if len(emp_ids_to_del) != 0:
                    emp_ids_to_del.write({'user_id': False})
                    # for emp_id in emp_ids_to_del:
                    #     if emp_id != res:
                    #         self.write(cr, SUPERUSER_ID, emp_id, {'user_id': False}, context)

                if cur_user:
                    cur_user.with_context(context_new).write({'eq_employee_id': res.id})
        return res

    @api.one
    def write(self, values):
        """

        :param values:
        :return:
        """
        context_new = {}
        if self._context:
            context_new = dict(self._context)
        context_new['do_not_repeat'] = True

        # if type(ids) is not list: ids = [ids]

        if 'user_id' in values and 'do_not_repeat' not in self._context:
            user_obj = self.env['res.users']
            if values['user_id']:
                if values['user_id'] != self.user_id.id:
                    # Removes the employee from all users, except the current one.
                    emp_ids_to_del = self.search([('user_id', '=', values['user_id'])])
                    if len(emp_ids_to_del) != 0:
                        for emp_id in emp_ids_to_del:
                            if emp_id.id != self.id:
                                emp_id.write({'user_id': False})
                    user_ids_to_clear = user_obj.search([('eq_employee_id', '=', self.id)])
                    if len(user_ids_to_clear) != 0:
                        user_ids_to_clear.with_context(context_new).write({'eq_employee_id': False})

                    # Sets the employee_id for the user.
                    user_to_update = user_obj.browse(values['user_id'])
                    if user_to_update:
                        user_to_update.with_context(context_new).write({'eq_employee_id': self.id})
            else:
                # Removes the employee from all the users.
                user_ids_to_clear = user_obj.search([('eq_employee_id', '=', self.id)])
                if user_ids_to_clear:
                    user_ids_to_clear.with_context(context_new).write({'eq_employee_id': False})

        res = super(eq_hr_employee, self).write(values)

        return res
