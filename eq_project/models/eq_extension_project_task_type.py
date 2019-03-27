# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class project_task_type_class(models.Model):
    """
    Extension of table project.task.type -> we're adding new boolean field here
    """
    _inherit = 'project.task.type'

    calculated_item = fields.Boolean("Calculable level",default=True)
