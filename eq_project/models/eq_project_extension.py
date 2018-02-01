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
    _inherit = 'project.project'




    @api.model
    def create(self, vals):
            seq = self.env['ir.sequence'].get('eq_project_number')
            vals['eq_project_number'] = seq
            return super(eq_project_extension, self).create(vals)



    @api.onchange('planned_hours')
    def _calculated_total_time(self):
         eq_total_hour = 0.0

         for project in self:
             task_obj = self.env['project.task'].search([('project_id', '=', project.id)])

             for task in task_obj:

                 if (task.stage_id.id != 1) and (task.stage_id.id != 2) and (task.stage_id.id != 3) and (task.stage_id.id != 4):  # wenn stage_id not on state  (new,abgeschlossen,basic,advanced)

                     eq_total_hour = task.planned_hours + eq_total_hour


                 else:
                     pass

             project.eq_total_hours = eq_total_hour
             eq_total_hour = 0.0

    @api.onchange('planned_hours, progress')
    def _calculated_rest_time(self):
        eq_rest_hour = 0.0

        for project in self:
              task_obj = self.env['project.task'].search([('project_id', '=', project.id)])

              for task in task_obj:
                  if (task.stage_id.id != 1) and (task.stage_id.id != 2) and (task.stage_id.id != 3) and (task.stage_id.id != 4):  # wenn stage_id not on state  (new,abgeschlossen,basic,advanced)

                      eq_rest_hour = (task.planned_hours-((task.progress *  task.planned_hours)/100) ) + eq_rest_hour #progress was in percent

                  else:
                      pass
              project.eq_rest_hours = eq_rest_hour
              eq_rest_hour= 0.0



    @api.onchange('progress')
    def _calculated_worked_time(self):
        eq_worked_hour = 0.0

        for project in self:
            task_obj = self.env['project.task'].search([('project_id', '=', project.id)])

            for task in task_obj:
                if (task.stage_id.id != 1) and (task.stage_id.id != 2) and (task.stage_id.id != 3) and (task.stage_id.id != 4):  # wenn stage_id not on state  (new,abgeschlossen,basic,advanced)
                        eq_worked_hour = ((task.progress *  task.planned_hours)/100 ) + eq_worked_hour #was in percent
                else:
                    pass
            project.eq_worked_hours = eq_worked_hour
            eq_worked_hour = 0.0

    @api.onchange('date_deadline')
    def _deadline_date(self):
        eq_date = ''
        for project in self:
             task_obj = self.env['project.task'].search([('project_id', '=', project.id)])

             for task in task_obj:

                 if (task.stage_id.id != 1) and (task.stage_id.id != 2) and (task.stage_id.id != 3) and (task.stage_id.id != 4): #wenn stage_id not on state  (new,abgeschlossen,basic,advanced)
                      if (task['date_deadline']) > eq_date :
                          eq_date = task['date_deadline']
                      else :
                          pass
                 else:
                     pass

             project.eq_deadline = eq_date
             eq_date = ''




    eq_project_number = fields.Char('Number')

    eq_deadline = fields.Date (string='Deadline Date', compute='_deadline_date')
    eq_rest_hours = fields.Float(string='rest Time', compute='_calculated_rest_time')
    eq_total_hours = fields.Float(string=' total Time', compute='_calculated_total_time')
    eq_worked_hours = fields.Float(string='worked Time', compute='_calculated_worked_time')

    eq_time_start = fields.Float(string='Begin Hour')
    eq_time_stop = fields.Float(string='End Hour')



class eq_project_extension_2(models.Model):
        _inherit = 'account.analytic.line'

        @api.onchange('project_id')
        def account_billiable(self):
              for account in self:
                   project_obj= self.env['project.project'].search([('id', '=', account.project_id)])

                   for id in  project_obj:
                       self.to_invoice = id.eq_to_invoice_id

















