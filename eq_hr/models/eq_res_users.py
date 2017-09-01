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


class eq_hr_res_users(models.Model):
    _inherit = 'res.users'

    eq_employee_id = fields.Many2one('hr.employee', 'Employee', copy=False)

    @api.model
    def create(self, values):

        ##### Überprüft, ob Flag in den Grundeinstellungen gesetzt ist und somit ein Versenden einer Reset-Passwort Email stattfinden soll
        # vorerst auskommentiert
        # ir_values = self.pool.get('ir.values')
        # reset_password = ir_values.get_default(cr, uid, 'res.users', 'default_reset_passwort')
        # if not reset_password:
        #     mycontext = dict(context)
        #     mycontext["no_reset_password"] = True
        # else:
        #     mycontext = dict(context)
        #     if 'no_reset_password' in mycontext:
        #         del mycontext['no_reset_password']
        #context = mycontext

        context_new = {}
        if self._context:
            context_new = dict(self._context)


        res = super(eq_hr_res_users, self).create(values)

        if 'eq_employee_id' in values and 'do_not_repeat' not in self._context:
            if values['eq_employee_id']:
                emp_obj = self.env['hr.employee']
                # Removes the user from all employees, except the selected one.
                user_ids_to_del = self.search([('eq_employee_id', '=', values['eq_employee_id'])])  # SUPERUSER_ID
                if len(user_ids_to_del) != 0:
                    for user_id in user_ids_to_del:
                        if user_id.id != res.id:
                            user_id.write({'eq_employee_id': False})  # SUPERUSER_ID
                # Sets the user_id in the employee. do_not_repeat in context so that the employee does not set the employee_id for the user.

                emp_to_update = emp_obj.browse(values['eq_employee_id'])
                if emp_to_update:
                    context_new['do_not_repeat'] = True
                    emp_to_update.with_context(context_new).write({'user_id': res.id})
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

        if 'eq_employee_id' in values and 'do_not_repeat' not in self._context:
            emp_obj = self.env['hr.employee']
            if values['eq_employee_id']:
                if values['eq_employee_id'] != self.eq_employee_id.id:
                    # Removes the user from all employees, except the selected one
                    user_ids_to_del = self.search([('eq_employee_id', '=', values['eq_employee_id'])])
                    print 'User user_ids_to_del', user_ids_to_del
                    if len(user_ids_to_del) != 0:
                        for user_id in user_ids_to_del:
                            if user_id.id != self.id:
                                user_id.write({'eq_employee_id': False})

                    # Benutzerfeld für Mitarbeiter leeren, für die bisher der aktuelle Benutzer gesetzt war
                    employees_to_clear = emp_obj.search([('user_id', '=', self.id)])
                    if len(employees_to_clear) != 0:
                        employees_to_clear.with_context(context_new).write({'user_id': False})

                    # Sets the user_id in the employee
                    emp_to_update = emp_obj.browse(values['eq_employee_id'])
                    emp_to_update.with_context(context_new).write({'user_id': self.id})
            else:
                # Removes the user from all employees
                employees_to_clear = emp_obj.search([('user_id', '=', self.id)])
                if employees_to_clear:
                    employees_to_clear.with_context(context_new).write({'user_id': False})

        res = super(eq_hr_res_users, self).write(values)

        return res