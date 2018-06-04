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

import logging

import threading

from ast import literal_eval

from odoo import api, fields, registry, models, _, SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.tools.misc import ustr

from odoo.addons.base.ir.ir_mail_server import MailDeliveryException
from odoo.addons.auth_signup.models.res_partner import SignupError, now

_logger = logging.getLogger(__name__)


class eq_res_users(models.Model):
    _inherit = 'res.users'

    @api.multi
    def action_reset_password(self):
        """ create signup token for each user, and send their signup url by email """
        # prepare reset password signup
        create_mode = bool(self.env.context.get('create_user'))

        # no time limit for initial invitation, only for reset password
        expiration = False if create_mode else now(days=+1)

        self.mapped('partner_id').signup_prepare(signup_type="reset", expiration=expiration)

        # send email to users with their signup url
        template = False
        if create_mode:
            try:
                template = self.env.ref('auth_signup.set_password_email', raise_if_not_found=False)
            except ValueError:
                pass
        if not template:
            template = self.env.ref('eq_mail_templates.eq_reset_password_email')
        assert template._name == 'mail.template'

        for user in self:
            if not user.email:
                raise UserError(_("Cannot send email: user %s has no email address.") % user.name)
            template.with_context(lang=user.lang).send_mail(user.id, force_send=True, raise_exception=True)
            _logger.info("Password reset email sent for user <%s> to <%s>", user.login, user.email)

class eq_res_partner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _notify_by_email(self, message, force_send=False, send_after_commit=True, user_signature=True):
        """ Method to send email linked to notified messages. The recipients are
        the recordset on which this method is called.

        :param boolean force_send: send notification emails now instead of letting the scheduler handle the email queue
        :param boolean send_after_commit: send notification emails after the transaction end instead of durign the
                                          transaction; this option is used only if force_send is True
        :param user_signature: add current user signature to notification emails """
        if not self.ids:
            return True

        # existing custom notification email
        base_template = None
        if message.model and self._context.get('custom_layout', False):
            base_template = self.env.ref(self._context['custom_layout'], raise_if_not_found=False)
        if not base_template:
            base_template = self.env.ref('eq_mail_templates.eq_mail_template_data_notification_email_default')

        base_template_ctx = self._notify_prepare_template_context(message)
        if not user_signature:
            base_template_ctx['signature'] = False
        base_mail_values = self._notify_prepare_email_values(message)

        # classify recipients: actions / no action
        if message.model and message.res_id and hasattr(self.env[message.model], '_message_notification_recipients'):
            recipients = self.env[message.model].browse(message.res_id)._message_notification_recipients(message, self)
        else:
            recipients = self.env['mail.thread']._message_notification_recipients(message, self)

        emails = self.env['mail.mail']
        recipients_nbr, recipients_max = 0, 50
        for email_type, recipient_template_values in recipients.iteritems():
            if recipient_template_values['followers']:
                # generate notification email content
                template_fol_values = dict(base_template_ctx,
                                           **recipient_template_values)  # fixme: set button_unfollow to none
                template_fol_values['has_button_follow'] = False
                template_fol = base_template.with_context(**template_fol_values)
                # generate templates for followers and not followers
                fol_values = template_fol.generate_email(message.id, fields=['body_html', 'subject'])
                # send email
                new_emails, new_recipients_nbr = self._notify_send(fol_values['body'], fol_values['subject'],
                                                                   recipient_template_values['followers'],
                                                                   **base_mail_values)
                # update notifications
                self._notify_udpate_notifications(new_emails)

                emails |= new_emails
                recipients_nbr += new_recipients_nbr
            if recipient_template_values['not_followers']:
                # generate notification email content
                template_not_values = dict(base_template_ctx,
                                           **recipient_template_values)  # fixme: set button_follow to none
                template_not_values['has_button_unfollow'] = False
                template_not = base_template.with_context(**template_not_values)
                # generate templates for followers and not followers
                not_values = template_not.generate_email(message.id, fields=['body_html', 'subject'])
                # send email
                new_emails, new_recipients_nbr = self._notify_send(not_values['body'], not_values['subject'],
                                                                   recipient_template_values['not_followers'],
                                                                   **base_mail_values)
                # update notifications
                self._notify_udpate_notifications(new_emails)

                emails |= new_emails
                recipients_nbr += new_recipients_nbr

        # NOTE:
        #   1. for more than 50 followers, use the queue system
        #   2. do not send emails immediately if the registry is not loaded,
        #      to prevent sending email during a simple update of the database
        #      using the command-line.
        test_mode = getattr(threading.currentThread(), 'testing', False)
        if force_send and recipients_nbr < recipients_max and \
                (not self.pool._init or test_mode):
            email_ids = emails.ids
            dbname = self.env.cr.dbname
            _context = self._context

            def send_notifications():
                db_registry = registry(dbname)
                with api.Environment.manage(), db_registry.cursor() as cr:
                    env = api.Environment(cr, SUPERUSER_ID, _context)
                    env['mail.mail'].browse(email_ids).send()

            # unless asked specifically, send emails after the transaction to
            # avoid side effects due to emails being sent while the transaction fails
            if not test_mode and send_after_commit:
                self._cr.after('commit', send_notifications)
            else:
                emails.send()

        return True