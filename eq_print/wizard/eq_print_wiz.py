# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
from odoo import models, fields, api

import odoo

class EqPrintWiz(models.TransientModel):
    """New class EqPrintWiz"""
    _name = 'eq.print.wiz'

    def _get_default_printer(self):
        user = self.env['res.users'].browse(self._uid)
        if user.eq_default_printer_id:
            return user.eq_default_printer_id.id
        return False

    def _get_default_user(self):
        if self._uid:
            return self._uid
        return False

    eq_printer_id = fields.Many2one(
        string="Printer",
        comodel_name="eq.printer",
        default=_get_default_printer,
        required=True)
    eq_copies = fields.Integer(string="Copies", default=1, required=True)
    eq_user_id = fields.Many2one(
        string="User",
        comodel_name="res.users",
        default=_get_default_user,
        required=True)

    @api.multi
    def print_document(self):
        active_ids = self.env.context['active_ids']

        #Anpassung für Pentaho
        act_report_xml_obj = self.env['ir.actions.report.xml']

        found_report = None
        if 'params' in self.env.context:
            if 'action' in self.env.context['params']:
                action = self.env.context['params']['action']
                seach_rep = act_report_xml_obj.search([('eq_report_wiz_action', '=', action)])
                if seach_rep:
                    found_report = act_report_xml_obj.browse(seach_rep.id)

        if found_report and found_report != None:
            if found_report.report_type in ['qweb-html', 'qweb-pdf']:
                # content, type = self.env['report'].get_pdf(self.env.cr, self.env.uid,
                #                                            active_ids, found_report.report_name,
                #                                             context=self.env.context), 'pdf'
                pdf_binary = self.env['report'].get_pdf(active_ids, self.env.context['report_name'])
            else:
                datas = {'model': self.env[self._context['active_model']]}
                pdf_binary, new_type = odoo.report.render_report(
                    active_ids,
                    found_report.report_name,
                    datas)
        else:
            pdf_binary = self.env['report'].get_pdf(active_ids, self.env.context['report_name'])

        encoded_pdf_binary = base64.b64encode(pdf_binary)
        current_obj = self.env[self._context['active_model']]
        current_obj_rec_name = current_obj._rec_name
        current_records = current_obj.browse(active_ids)
        document_name = ""
        if len(current_records) == 1:
            document_name = getattr(current_records, current_obj_rec_name)
        elif len(current_records) > 1:
            document_name = "%sx %s" % (len(current_records), current_obj._description)
        spooltable_vals = {
            'eq_printer_id': self.eq_printer_id.id,
            'eq_user_id': self.eq_user_id.id,
            'eq_copies': self.eq_copies,
            'eq_file': encoded_pdf_binary,
            'eq_document_name': document_name,
            'state': 'open',
            }
        self.env['eq.spooltable'].create(spooltable_vals)
        return True
