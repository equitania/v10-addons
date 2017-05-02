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
from openerp import SUPERUSER_ID
import time
from imaplib import IMAP4
from imaplib import IMAP4_SSL
from poplib import POP3
from poplib import POP3_SSL
from openerp.tools import frozendict
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

import zipfile
import base64
from openerp import addons

from openerp.addons.base.ir.ir_mail_server import MailDeliveryException
from openerp.osv import fields, osv
from openerp import tools, api
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

class eq_fetchmail_server(osv.Model):
    _inherit = "fetchmail.server"
    
    _columns = {
        'user_id': fields.many2one('res.users', string="Owner"),
    }
    
    #Copy and Pasted form original fetchmail.server and removed the remove E-Mail for pop mail servers.
    def fetch_mail(self, cr, uid, ids, context=None):
        """WARNING: meant for cron usage only - will commit() after each email!"""
        context = dict(context or {})
        context['fetchmail_cron_running'] = True
        mail_thread = self.pool.get('mail.thread')
        action_pool = self.pool.get('ir.actions.server')
        for server in self.browse(cr, uid, ids, context=context):
            _logger.info('start checking for new emails on %s server %s', server.type, server.name)
            context.update({'fetchmail_server_id': server.id, 'server_type': server.type})
            count, failed = 0, 0
            imap_server = False
            pop_server = False
            if server.type == 'imap':
                try:
                    imap_server = server.connect()
                    imap_server.select()
                    result, data = imap_server.search(None, '(UNSEEN)')
                    for num in data[0].split():
                        res_id = None
                        result, data = imap_server.fetch(num, '(RFC822)')
                        imap_server.store(num, '-FLAGS', '\\Seen')
                        try:
                            res_id = mail_thread.message_process(cr, uid, server.object_id.model,
                                                                 data[0][1],
                                                                 save_original=server.original,
                                                                 strip_attachments=(not server.attach),
                                                                 context=context)
                        except Exception:
                            _logger.exception('Failed to process mail from %s server %s.', server.type, server.name)
                            failed += 1
                        if res_id and server.action_id:
                            action_pool.run(cr, uid, [server.action_id.id], {'active_id': res_id, 'active_ids': [res_id], 'active_model': context.get("thread_model", server.object_id.model)})
                        imap_server.store(num, '+FLAGS', '\\Seen')
                        cr.commit()
                        count += 1
                    _logger.info("Fetched %d email(s) on %s server %s; %d succeeded, %d failed.", count, server.type, server.name, (count - failed), failed)
                except Exception:
                    _logger.exception("General failure when trying to fetch mail from %s server %s.", server.type, server.name)
                finally:
                    if imap_server:
                        imap_server.close()
                        imap_server.logout()
            elif server.type == 'pop':
                try:
                    pop_server = server.connect()
                    (numMsgs, totalSize) = pop_server.stat()
                    pop_server.list()
                    for num in range(1, numMsgs + 1):
                        (header, msges, octets) = pop_server.retr(num)
                        msg = '\n'.join(msges)
                        res_id = None
                        try:
                            res_id = mail_thread.message_process(cr, uid, server.object_id.model,
                                                                 msg,
                                                                 save_original=server.original,
                                                                 strip_attachments=(not server.attach),
                                                                 context=context)
                        except Exception:
                            _logger.exception('Failed to process mail from %s server %s.', server.type, server.name)
                            failed += 1
                        if res_id and server.action_id:
                            action_pool.run(cr, uid, [server.action_id.id], {'active_id': res_id, 'active_ids': [res_id], 'active_model': context.get("thread_model", server.object_id.model)})
                        cr.commit()
                    _logger.info("Fetched %d email(s) on %s server %s; %d succeeded, %d failed.", numMsgs, server.type, server.name, (numMsgs - failed), failed)
                except Exception:
                    _logger.exception("General failure when trying to fetch mail from %s server %s.", server.type, server.name)
                finally:
                    if pop_server:
                        pop_server.quit()
            server.write({'date': time.strftime(tools.DEFAULT_SERVER_DATETIME_FORMAT)})
        return True

class eq_ir_mail_server(osv.Model):
    _inherit = "ir.mail_server"
    
    _columns = {
        'user_id': fields.many2one('res.users', string="Owner"),
    }
        
class eq_mail_mail(osv.Model):
    _inherit = 'mail.mail'
    
    _columns = {
        'mail_server_id': fields.many2one('ir.mail_server', "Default Mail Server"),
        'mail_server_address': fields.char('Default Mail Server Address'),
    }
    
    _default = {
                lambda self, cr, uid, context: self.pool.get('ir.values').get_default(cr, uid, 'mail.mail', 'mail_server_id'),
                lambda self, cr, uid, context: self.pool.get('ir.values').get_default(cr, uid, 'mail.mail', 'mail_server_address'),
                }
    
    
    
    
    def send(self, cr, uid, ids, auto_commit=False, raise_exception=False, context=None):
        """ Sends the selected emails immediately, ignoring their current
            state (mails that have already been sent should not be passed
            unless they should actually be re-sent).
            Emails successfully delivered are marked as 'sent', and those
            that fail to be deliver are marked as 'exception', and the
            corresponding error mail is output in the server logs.

            :param bool auto_commit: whether to force a commit of the mail status
                after sending each mail (meant only for scheduler processing);
                should never be True during normal transactions (default: False)
            :param bool raise_exception: whether to raise an exception if the
                email sending process has failed
            :return: True
        """

        context = dict(context or {})
        ir_mail_server = self.pool.get('ir.mail_server')
        ir_attachment = self.pool['ir.attachment']
        ir_values = self.pool.get('ir.values')
       
        
        default_mail_server = ir_values.get_default(cr, uid, 'mail.mail', 'mail_server_id')
        #default_mail_address = ir_values.get_default(cr, uid, 'mail.mail', 'mail_server_address')
        ######
        existing_ir_mail_server = self.pool.get('ir.mail_server').search(cr,uid,[('id','=',default_mail_server)])
        if existing_ir_mail_server != []:
            address = self.pool.get('ir.mail_server').browse(cr, uid,  default_mail_server, context=context)
            default_mail_address = getattr(address, "smtp_user", False)
        else:
            address = False
            default_mail_address = False
            
        
        ########
        for mail in self.browse(cr, SUPERUSER_ID, ids, context=context):
            try:
                # TDE note: remove me when model_id field is present on mail.message - done here to avoid doing it multiple times in the sub method
                if mail.model:
                    model_id = self.pool['ir.model'].search(cr, SUPERUSER_ID, [('model', '=', mail.model)], context=context)[0]
                    model = self.pool['ir.model'].browse(cr, SUPERUSER_ID, model_id, context=context)
                else:
                    model = None
                if model:
                    context['model_name'] = model.name

                # load attachment binary data with a separate read(), as prefetching all
                # `datas` (binary field) could bloat the browse cache, triggerring
                # soft/hard mem limits with temporary data.
                attachment_ids = [a.id for a in mail.attachment_ids]
                attachments = [(a['datas_fname'], base64.b64decode(a['datas']))
                                 for a in ir_attachment.read(cr, SUPERUSER_ID, attachment_ids,
                                                             ['datas_fname', 'datas'])]

                # specific behavior to customize the send email for notified partners
                email_list = []
                if mail.email_to:
                    email_list.append(self.send_get_email_dict(cr, uid, mail, context=context))
                for partner in mail.recipient_ids:
                    email_list.append(self.send_get_email_dict(cr, uid, mail, partner=partner, context=context))
                # headers
                headers = {}
                bounce_alias = self.pool['ir.config_parameter'].get_param(cr, uid, "mail.bounce.alias", context=context)
                catchall_domain = self.pool['ir.config_parameter'].get_param(cr, uid, "mail.catchall.domain", context=context)

### Übernahme der Anpassung vom Equitania Modul (siehe ReleaseNotes des Equitania Moduls vom 15.01.2016)               
                if bounce_alias and catchall_domain:
                    headers['Return-Path'] = '%s@%s' % (bounce_alias, catchall_domain)
                else:
                    headers['Return-Path'] = mail.email_from
                
#### Kern-Version                
#                 if bounce_alias and catchall_domain:
#                     if mail.model and mail.res_id:
#                         headers['Return-Path'] = '%s-%d-%s-%d@%s' % (bounce_alias, mail.id, mail.model, mail.res_id, catchall_domain)
#                     else:
#                         headers['Return-Path'] = '%s-%d@%s' % (bounce_alias, mail.id, catchall_domain)
                        
                        
                        
                        
                if mail.headers:
                    try:
                        headers.update(eval(mail.headers))
                    except Exception:
                        pass

                # Writing on the mail object may fail (e.g. lock on user) which
                # would trigger a rollback *after* actually sending the email.
                # To avoid sending twice the same email, provoke the failure earlier
                mail.write({'state': 'exception'})
                mail_sent = False

                # build an RFC2822 email.message.Message object and send it without queuing
                res = None
                mail_server = False
                user = context.get('user_id', SUPERUSER_ID)

                if user != SUPERUSER_ID:
                    mail_server = ir_mail_server.search(cr, uid, [('user_id', '=', user)], context=context)
                
                for email in email_list:
                    if not mail_server and default_mail_address:
                        msg = ir_mail_server.build_email(
                            email_from=default_mail_address,
                            email_to=email.get('email_to'),
                            subject=email.get('subject'),
                            body=email.get('body'),
                            body_alternative=email.get('body_alternative'),
                            email_cc=tools.email_split(mail.email_cc),
                            reply_to=mail.email_from,
                            attachments=attachments,
                            message_id=mail.message_id,
                            references=mail.references,
                            object_id=mail.res_id and ('%s-%s' % (mail.res_id, mail.model)),
                            subtype='html',
                            subtype_alternative='plain',
                            headers=headers)
                        msg['Return-Path'] = default_mail_address
                        res = ir_mail_server.send_email(cr, uid, msg,
                                                        mail_server_id=default_mail_server,
                                                        context=context)
                    else:
                        msg = ir_mail_server.build_email(
                            email_from=mail.email_from,
                            email_to=email.get('email_to'),
                            subject=email.get('subject'),
                            body=email.get('body'),
                            body_alternative=email.get('body_alternative'),
                            email_cc=tools.email_split(mail.email_cc),
                            reply_to=mail.email_from,
                            attachments=attachments,
                            message_id=mail.message_id,
                            references=mail.references,
                            object_id=mail.res_id and ('%s-%s' % (mail.res_id, mail.model)),
                            subtype='html',
                            subtype_alternative='plain',
                            headers=headers)
                        msg['Return-Path'] = mail.email_from
                        res = ir_mail_server.send_email(cr, uid, msg,
                                                        mail_server_id=mail_server[0],
                                                        context=context)

                if res:
                    mail.write({'state': 'sent', 'message_id': res})
                    mail_sent = True

                # /!\ can't use mail.state here, as mail.refresh() will cause an error
                # see revid:odo@openerp.com-20120622152536-42b2s28lvdv3odyr in 6.1
                if mail_sent:
                    _logger.info('Mail with ID %r and Message-Id %r successfully sent', mail.id, mail.message_id)
                self._postprocess_sent_message(cr, uid, mail, context=context, mail_sent=mail_sent)
            except MemoryError:
                # prevent catching transient MemoryErrors, bubble up to notify user or abort cron job
                # instead of marking the mail as failed
                _logger.exception('MemoryError while processing mail with ID %r and Msg-Id %r. '\
                                      'Consider raising the --limit-memory-hard startup option',
                                  mail.id, mail.message_id)
                raise
            except Exception as e:
                _logger.exception('failed sending mail.mail %s', mail.id)
                mail.write({'state': 'exception'})
                self._postprocess_sent_message(cr, uid, mail, context=context, mail_sent=False)
                if raise_exception:
                    if isinstance(e, AssertionError):
                        # get the args of the original error, wrap into a value and throw a MailDeliveryException
                        # that is an except_orm, with name and value as arguments
                        value = '. '.join(e.args)
                        raise MailDeliveryException(_("Mail Delivery Failed"), value)
                    raise

            if auto_commit is True:
                cr.commit()
        return True
    
class eq_mail_followers(osv.Model):
    _inherit = "mail.notification"
            
    def _notify(self, cr, uid, message_id, partners_to_notify=None, context=None,
                force_send=False, user_signature=True):
        """ Send by email the notification depending on the user preferences

            :param list partners_to_notify: optional list of partner ids restricting
                the notifications to process
            :param bool force_send: if True, the generated mail.mail is
                immediately sent after being created, as if the scheduler
                was executed for this message only.
            :param bool user_signature: if True, the generated mail.mail body is
                the body of the related mail.message with the author's signature
        """
        notif_ids = self.search(cr, SUPERUSER_ID, [('message_id', '=', message_id), ('partner_id', 'in', partners_to_notify)], context=context)
        
        # update or create notifications
        new_notif_ids = self.update_message_notification(cr, SUPERUSER_ID, notif_ids, message_id, partners_to_notify, context=context)

        # mail_notify_noemail (do not send email) or no partner_ids: do not send, return
        if context and context.get('mail_notify_noemail', False):
            return True
        
        if not isinstance(context, frozendict):
            context['user_id'] = uid

        # browse as SUPERUSER_ID because of access to res_partner not necessarily allowed
        self._notify_email(cr, SUPERUSER_ID, new_notif_ids, message_id, force_send, user_signature, context=context)
        
class eq_res_user_extension(osv.osv):
    _inherit = 'res.users'
    
    def open_change_email(self, cr, uid, ids, context=None):
        mod_obj = self.pool.get('ir.model.data')
        res = mod_obj.get_object_reference(cr, uid, 'eq_mail_extension', 'eq_mail_password_change_form')
                
        return {
                'name': 'Neue Version',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': [res and res[1] or False],
                'res_model': 'eq_mail.password_change',                
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'context': "{}",
                'res_id': False,
            }

class eq_mail_password_change(osv.osv_memory):
    _name = "eq_mail.password_change"
    
    _columns = {
                'eq_old_password': fields.char('Old password', size=64,),
                'eq_password': fields.char('New password', size=64),
                'eq_compare_password': fields.char('Repeat new password', size=64),
                }
    
    def button_confirm(self, cr, uid, ids, context=None):
        #ir.mail_server Object and Dataset id for the user.
        ir_mail_server_obj = self.pool.get('ir.mail_server')
        ir_mail_server_id = ir_mail_server_obj.search(cr, SUPERUSER_ID, [('user_id','=', uid)])
        #fetchmail.server Object and Dataset id for the user.
        fetchmail_server_obj = self.pool.get('fetchmail.server')
        fetchmail_server_id = fetchmail_server_obj.search(cr, SUPERUSER_ID, [('user_id', '=', uid)])
        #eq_mail.password_change Dataset
        password = self.browse(cr, uid, ids, context)
        #ir.mail_server Dataset
        ir_mail_server = ir_mail_server_obj.browse(cr, SUPERUSER_ID, ir_mail_server_id, context)
        
        if len(ir_mail_server_id) == 0 and len(fetchmail_server_id) == 0:
            raise osv.except_osv(_('Error!'),_('There is no incoming and outgoing mailserver for this user./nPlease contact an administrator.' ))
        elif len(ir_mail_server_id) == 0:
            raise osv.except_osv(_('Error!'),_('There is no outgoing mailserver for this user./nPlease contact an administrator.' ))
        else:
            if password.eq_old_password != ir_mail_server.smtp_pass:
                raise osv.except_osv(_('Error!'),_('The old password does not match.' ))
            else:
                if password.eq_password != password.eq_compare_password:
                    raise osv.except_osv(_('Error!'),_('The two new passwords do not match.' ))
                else:
                    #Set password for ir_mail_server
                    ir_mail_server_values = {
                              'smtp_pass': password.eq_password,
                              }
                    ir_mail_server_obj.write(cr, SUPERUSER_ID, ir_mail_server_id, ir_mail_server_values, context)
                    if len(fetchmail_server_id) != 0:
                    #Set password for fetchmail_server
                        fetchmail_server_values = {
                                  'password': password.eq_password,
                                  }
                        fetchmail_server_obj.write(cr, uidSUPERUSER_ID, fetchmail_server_id, fetchmail_server_values, context)
                    return True