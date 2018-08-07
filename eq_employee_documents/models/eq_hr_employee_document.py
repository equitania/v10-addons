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
import os
import base64
class eq_hr_employee_document(models.Model):
    _inherit = 'hr.employee.document'

    image_small = fields.Binary("File Format", attachment=True,
                                help="Small-sized photo of the document type. It is automatically "
                                     "resized as a 64x64px image, with aspect ratio preserved. "
                                     "Use this field anywhere a small image is required.")

    @api.model
    def _create_sequence(self):
        """
        Function for document number sequence creation
        """
        self.env["ir.sequence"].create(
            {"name": "EQ Employee Documents", "code": "hr.employee.document", "prefix": "Document No.:", "padding": 5,
             "number_increment": 1,
             "numer_nex_actual": 1})


    @api.model
    def create(self, vals):
        """
        Overrided base create function for document number sequence creation and showing image for file format
        :param vals: vals
        :return: result
        """
        image_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'static/img'))

        attachment_id = vals['doc_attachment_id'][0][2][0]
        attachment_name = self.env['ir.attachment'].search([('id','=', attachment_id)]).name
        file_format = attachment_name.split('.')[1]

        try:
            with open(image_path+"/"+file_format+".png", "rb") as image_file:
                image = base64.b64encode(image_file.read())
            vals['image_small'] = image
        except:
            print('There is no image for this file format')

        vals['name'] = self.env['ir.sequence'].next_by_code('hr.employee.document')
        result = super(eq_hr_employee_document, self).create(vals)
        return result
