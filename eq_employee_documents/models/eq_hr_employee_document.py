# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
import base64
from odoo import models, fields, api

class EqHrEmployeeDocument(models.Model):
    """
    Inherited HrEmployeeDocument class
    """
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
            {"name": "EQ Employee Documents",
             "code": "hr.employee.document",
             "prefix": "Document No.:",
             "padding": 5,
             "number_increment": 1,
             "numer_nex_actual": 1})


    @api.model
    def create(self, vals):
        """
        Overrided base create function for document number sequence creation
        and showing image for file format
        :param vals: vals
        :return: result
        """
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static/img'))

        if 'doc_attachment_id' in vals and vals['doc_attachment_id']:
            if vals['doc_attachment_id'][0][2]:
                attachment_id = vals['doc_attachment_id'][0][2][0]
                attachment_name = self.env['ir.attachment'].search([('id', '=', attachment_id)]).name
                file_format = attachment_name.split('.')[1]

                try:
                    with open(image_path+"/"+file_format+".png", "rb") as image_file:
                        image = base64.b64encode(image_file.read())
                    vals['image_small'] = image
                except:
                    print 'There is no image for this file format'

        vals['name'] = self.env['ir.sequence'].next_by_code('hr.employee.document')
        result = super(EqHrEmployeeDocument, self).create(vals)
        return result

    @api.multi
    def write(self, vals):
        """
           Overrided base write function for showing image for file format
           :param vals: vals
           :return: result
        """
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static/img'))

        if 'doc_attachment_id' in vals and vals['doc_attachment_id']:
            if vals['doc_attachment_id'][0][2]:
                attachment_id = vals['doc_attachment_id'][0][2][0]
                attachment_name = self.env['ir.attachment'].search([('id', '=', attachment_id)]).name
                file_format = attachment_name.split('.')[1]

                try:
                    with open(image_path + "/" + file_format + ".png", "rb") as image_file:
                        image = base64.b64encode(image_file.read())
                    vals['image_small'] = image
                except:
                    print 'There is no image for this file format'

        result = super(EqHrEmployeeDocument, self).write(vals)
        return result
