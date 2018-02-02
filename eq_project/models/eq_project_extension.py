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
from datetime import datetime as DateTime


class eq_project_extension(models.Model):
    """
    this class is used to calculate the time fields that will be displayed in the kanban

    """
    _inherit = 'project.project'


    eq_project_number = fields.Char('Number')

    eq_deadline = fields.Date (string='Deadline Date', compute='_deadline_date')
    eq_rest_hours = fields.Float(string='rest Time', compute='_calculated_rest_time')
    eq_total_hours = fields.Float(string=' total Time', compute='_calculated_total_time')
    eq_worked_hours = fields.Float(string='worked Time', compute='_calculated_worked_time')

    eq_time_start = fields.Float(string='Begin Hour')
    eq_time_stop = fields.Float(string='End Hour')



    @api.model
    def create(self, vals):
        """
        This overwrites the create method. give a project number automatically

        :param vals:
        :return:
        """

        seq = self.env['ir.sequence'].get('eq_project_number')
        vals['eq_project_number'] = seq
        return super(eq_project_extension, self).create(vals)


    def nummer_generator(self):
        """
        give a project number automatically, if not set
        :return:
        """
        seq = self.env['ir.sequence'].get('eq_project_number')
        self.eq_project_number = seq




    @api.onchange('eq_total_hours') #planned_hours
    def _calculated_total_time(self):
        """
            calculate the total time invested in the project
        :return:
        """
        eq_total_hour = 0.0
        for project in self:
             task_obj = self.env['project.task'].search([('project_id', '=', project.id)])

             for task in task_obj:

                 if (task.stage_id.calculated_item):  # wenn stage_id only on state  (start & Umsetzung)

                     eq_total_hour = task.planned_hours + eq_total_hour


                 else:
                     pass

             project.eq_total_hours = eq_total_hour
             eq_total_hour = 0.0

    @api.onchange('eq_total_hours','eq_worked_hours') #planned_hours, progress
    def _calculated_rest_time(self):
        """
        calculate the working time invested in the project
        :param self:
        :return:
        """
        eq_rest_hour = 0.0

        for project in self:
              task_obj = self.env['project.task'].search([('project_id', '=', project.id)])

              for task in task_obj:
                  if (task.stage_id.calculated_item):  # wenn stage_id only on state  (start & Umsetzung)
                      eq_rest_hour = (task.planned_hours-((task.progress *  task.planned_hours)/100) ) + eq_rest_hour #progress was in percent

                  else:
                      pass
              project.eq_rest_hours = eq_rest_hour
              eq_rest_hour= 0.0



    @api.onchange('eq_worked_hours')
    def _calculated_worked_time(self):
        """
        calculate the remaining work time to invest in the project
        :param self:
        :return:
        """
        eq_worked_hour = 0.0

        for project in self:
            task_obj = self.env['project.task'].search([('project_id', '=', project.id)])

            for task in task_obj:
                if (task.stage_id.calculated_item):  # wenn stage_id only on state  (start & Umsetzung)
                    eq_worked_hour = ((task.progress *  task.planned_hours)/100 ) + eq_worked_hour #was in percent
                else:
                    pass
            project.eq_worked_hours = eq_worked_hour
            eq_worked_hour = 0.0









class eq_project_extension_2(models.Model):
        _inherit = 'account.analytic.line'

        @api.onchange('project_id')
        def account_billiable(self):
            """
            ensures that the field eq_to_invoice_id  automatically recorded in the account.analytic.line
            :return:
            """
            for account in self:
               project_obj= self.env['project.project'].search([('id', '=', account.project_id.id)])

               for obj in  project_obj:
                   self.to_invoice = obj.eq_to_invoice_id

















