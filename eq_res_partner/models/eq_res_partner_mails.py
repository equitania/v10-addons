# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

class eq_res_partner_mails(models.Model):
    _inherit = 'res.partner'

    eq_received_mails = fields.Integer(string='Received Mails', compute='eq_received_mails_count', default=0)
    eq_send_mails = fields.Integer(string='Send Mails', compute='eq_send_mails_count', default=0)

    def eq_received_mails_count(self):
        object = self.env['mail.message']
        for partner in self:
            record = object.search([('partner_ids','in',partner.id)])
            message_count = len(record)
            partner.eq_received_mails = str(message_count)


    @api.multi
    def eq_send_mails_count(self):
        # Counting the number of received mails
        for res in self:
            mails = self.env['mail.message'].search([('author_id','=',res.id)])
            if len(mails) > 0:
                res.eq_send_mails = len(mails)
            else:
                res.eq_send_mails = 0

    @api.multi
    def eq_act_view_count_received_mails(self):
        # Showing the tree view with the messages sent to the current customer after click on the button Send Mails

        tree_view_id = self.env.ref('mail.view_message_tree').id
        form_view_id = self.env.ref('mail.view_message_form').id
        return {
            'name': 'Send Mails',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'views': [(tree_view_id, 'tree'),(form_view_id,'form')],
            'res_model': 'mail.message',
            'view_id': tree_view_id,
            'type': 'ir.actions.act_window',
            'domain': [('partner_ids','in', self.id)],
        }

    @api.multi
    def eq_act_view_count_send_mails(self):
        # Showing the tree view with the messages received from the current customer after click on the button Received Mails

        tree_view_id = self.env.ref('mail.view_message_tree').id
        form_view_id = self.env.ref('mail.view_message_form').id
        return {
            'name': 'Received Mails',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
            'res_model': 'mail.message',
            'view_id': tree_view_id,
            'type': 'ir.actions.act_window',
            'domain': [('author_id', '=', self.id)],

        }
