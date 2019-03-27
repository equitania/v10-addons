# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _


class eq_crm_lead(models.Model):
    """
    Extension of crm.lead class
    """
    _inherit = 'crm.lead'

    def _compute_count_quotations(self):
        """
        Calculate count of quotations for actual crm.lead
        :return: Count of quotation for actual crm.lead
        """
        sale_order_obj = self.env['sale.order']
        for crm in self:
            record = sale_order_obj.search([('partner_id', '=', crm.partner_id.id), ('state', 'in', ['draft', 'sent', 'cancel'])])
            crm_quot_count = len(record)
            crm.eq_count_quotations = str(crm_quot_count)

    def _compute_count_orders(self):
        """
        Calculate count of orders for actual crm.lead
        :return: Count of orders for actual crm.lead
        """
        sale_order_obj = self.env['sale.order']
        for crm in self:
            record = sale_order_obj.search([('partner_id', '=', crm.partner_id.id), ('state', 'not in', ['draft', 'sent', 'cancel'])])
            crm_quot_count = len(record)
            crm.eq_count_orders = str(crm_quot_count)

    def compute_quot_crm_count(self):
        """
        Obsolete ???
        """
        sale_order_obj = self.env['sale.order']
        for crm in self:
            record = sale_order_obj.search([('partner_id', '=', crm.partner_id.id)])
            crm_quot_count = len(record)
            crm.eq_count_quotations = str(crm_quot_count)

    eq_count_quotations = fields.Integer(compute='_compute_count_quotations', string="Number of Quotations")
    eq_count_orders = fields.Integer(compute='_compute_count_orders', string="Number of Orders")
    total_quot_crm = fields.Char(compute='compute_quot_crm_count', string="Quotations")
