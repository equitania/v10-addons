# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

#from openerp.osv import fields, osv
from openerp import fields,models

class eq_import_helper(models.Model):
    _name = 'eq_import_helper'
    

    ir_model =  fields.Many2one('ir.model')
    old_id = fields.Integer('Old id')
    new_id = fields.Integer('New id')
