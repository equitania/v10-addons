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

import babel.dates
import collections
from datetime import datetime, timedelta
from dateutil import parser
from dateutil import rrule
from dateutil.relativedelta import relativedelta
import logging
from operator import itemgetter
import pytz
import re
import time
import uuid

from odoo import api, fields, models
from odoo import tools
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, ValidationError


_logger = logging.getLogger(__name__)

class eqMeeting(models.Model):
    _inherit = 'calendar.event'

    @api.multi
    def write(self, values):
        # compute duration, only if start and stop are modified
        if not 'duration' in values and 'start' in values and 'stop' in values:
            values['duration'] = self._get_duration(values['start'], values['stop'])
        # process events one by one
        for meeting in self:
            # special write of complex IDS
            real_ids = []
            new_ids = []
            if not is_calendar_id(meeting.id):
                real_ids = [int(meeting.id)]
            else:
                real_event_id = calendar_id2real_id(meeting.id)

                # if we are setting the recurrency flag to False or if we are only changing fields that
                # should be only updated on the real ID and not on the virtual (like message_follower_ids):
                # then set real ids to be updated.
                blacklisted = any(key in values for key in ('start', 'stop', 'active'))
                if not values.get('recurrency', True) or not blacklisted:
                    real_ids = [real_event_id]
                else:
                    data = meeting.read(['start', 'stop', 'rrule', 'duration'])[0]
                    if data.get('rrule'):
                        new_ids = meeting.with_context(dont_notify=True).detach_recurring_event \
                            (values).ids  # to prevent multiple notify_next_alarm

            new_meetings = self.browse(new_ids)
            real_meetings = self.browse(real_ids)
            all_meetings = real_meetings + new_meetings
            super(Meeting, real_meetings).write(values)

            # set end_date for calendar searching
            if any(field in values for field in ['recurrency', 'end_type', 'count', 'rrule_type', 'start', 'stop']):
                for real_meeting in real_meetings:
                    if real_meeting.recurrency and real_meeting.end_type in ('count', unicode('count')):
                        final_date = real_meeting._get_recurrency_end_date()
                        super(Meeting, real_meeting).write({'final_date': final_date})

            attendees_create = False
            if values.get('partner_ids', False):
                attendees_create = all_meetings.with_context \
                    (dont_notify=True).create_attendees()  # to prevent multiple notify_next_alarm

            # Notify attendees if there is an alarm on the modified event, or if there was an alarm
            # that has just been removed, as it might have changed their next event notification
            if not self._context.get('dont_notify'):
                if len(meeting.alarm_ids) > 0 or values.get('alarm_ids'):
                    partners_to_notify = meeting.partner_ids.ids
                    event_attendees_changes = attendees_create and real_ids and attendees_create[real_ids[0]]
                    if event_attendees_changes:
                        partners_to_notify.extend(event_attendees_changes['removed_partners'].ids)
                    self.env['calendar.alarm_manager'].notify_next_alarm(partners_to_notify)

            if (values.get('start_date') or values.get('start_datetime') or
                (values.get('start') and self.env.context.get('from_ui'))) and values.get('active', True):
                for current_meeting in all_meetings:
                    if attendees_create:
                        attendees_create = attendees_create[current_meeting.id]
                        attendee_to_email = attendees_create['old_attendees'] - attendees_create['removed_attendees']
                    else:
                        attendee_to_email = current_meeting.attendee_ids

                    if attendee_to_email:
                        attendee_to_email._send_mail_to_attendees('eq_mail_templates.equitania_calendar_template_meeting_changedate')
        return True

    @api.multi
    def create_attendees(self):
        current_user = self.env.user
        result = {}
        for meeting in self:
            alreay_meeting_partners = meeting.attendee_ids.mapped('partner_id')
            meeting_attendees = self.env['calendar.attendee']
            meeting_partners = self.env['res.partner']
            for partner in meeting.partner_ids.filtered(lambda partner: partner not in alreay_meeting_partners):
                values = {
                    'partner_id': partner.id,
                    'email': partner.email,
                    'event_id': meeting.id,
                }

                # current user don't have to accept his own meeting
                if partner == self.env.user.partner_id:
                    values['state'] = 'accepted'

                attendee = self.env['calendar.attendee'].create(values)

                meeting_attendees |= attendee
                meeting_partners |= partner

            if meeting_attendees:
                to_notify = meeting_attendees.filtered(lambda a: a.email != current_user.email)
                to_notify._send_mail_to_attendees('eq_mail_templates.equitania_calendar_template_meeting_invitation')

                meeting.write({'attendee_ids': [(4, meeting_attendee.id) for meeting_attendee in meeting_attendees]})
            if meeting_partners:
                meeting.message_subscribe(partner_ids=meeting_partners.ids)

            # We remove old attendees who are not in partner_ids now.
            all_partners = meeting.partner_ids
            all_partner_attendees = meeting.attendee_ids.mapped('partner_id')
            old_attendees = meeting.attendee_ids
            partners_to_remove = all_partner_attendees + meeting_partners - all_partners

            attendees_to_remove = self.env["calendar.attendee"]
            if partners_to_remove:
                attendees_to_remove = self.env["calendar.attendee"].search(
                    [('partner_id', 'in', partners_to_remove.ids), ('event_id', '=', meeting.id)])
                attendees_to_remove.unlink()

            result[meeting.id] = {
                'new_attendees': meeting_attendees,
                'old_attendees': old_attendees,
                'removed_attendees': attendees_to_remove,
                'removed_partners': partners_to_remove
            }
        return result

    @api.multi
    def action_sendmail(self):
        email = self.env.user.email
        if email:
            for meeting in self:
                meeting.attendee_ids._send_mail_to_attendees('eq_mail_templates.equitania_calendar_template_meeting_invitation')
        return True

    def do_mail_reminder(self, alert):
        meeting = self.env['calendar.event'].browse(alert['event_id'])
        alarm = self.env['calendar.alarm'].browse(alert['alarm_id'])

        result = False
        if alarm.type == 'email':
            result = meeting.attendee_ids.filtered(lambda r: r.state != 'declined')._send_mail_to_attendees('eq_mail_templates.equitania_calendar_template_meeting_reminder', force_send=True)
        return result