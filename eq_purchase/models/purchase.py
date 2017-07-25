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


class eq_purchase_order(models.Model):
    _inherit = 'purchase.order'

    eq_head_text = fields.Html('Head Text')
    notes = fields.Html('Terms and conditions')

    # Report
    show_delivery_date = fields.Boolean(string='Show Delivery Date')
    use_calendar_week = fields.Boolean('Use Calendar Week for Delivery Date[equitania]')

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """
        Override für Wechsel der Partner_ID: Übernahme der custom-Felder
        :return:
        """

        super(eq_purchase_order, self).onchange_partner_id()

        partner = self.partner_id
        if partner:
            self.partner_ref = partner.eq_foreign_ref_purchase


class eq_purchase_order_line(models.Model):
    _inherit = 'purchase.order.line'

    @api.multi
    def _get_delivery_date(self):
        """
        Hilfsfunktion für Report für Ermittlung des Lieferdatums
        Aktuell wird Feld show_delivery_date der purchase_order nicht gesetzt -> Rückgabe immer false
        :return:
        """
        result = {}
        for purchase_line in self:
            if purchase_line.order_id.show_delivery_date and purchase_line.date_planned:
                delivery_date = datetime.strptime(purchase_line.date_planned, OE_DFORMAT)
                if purchase_line.order_id.partner_id.eq_delivery_date_type_purchase:
                    if purchase_line.order_id.partner_id.eq_delivery_date_type_purchase == 'cw':
                        result[purchase_line.id] = 'KW ' + delivery_date.strftime('%V/%Y')
                    elif purchase_line.order_id.partner_id.eq_delivery_date_type_purchase == 'date':
                        result[purchase_line.id] = delivery_date.strftime('%d.%m.%Y')
                else:
                    if purchase_line.order_id.use_calendar_week:
                        result[purchase_line.id] = 'KW ' + delivery_date.strftime('%V/%Y')
                    else:
                        result[purchase_line.id] = delivery_date.strftime('%d.%m.%Y')
            else:
                result[purchase_line.id] = False
        return result

class eq_purchase_configuration_address(models.TransientModel):
    _inherit = 'purchase.config.settings'
    # _inherit = _name

    def set_default_values(self):
        ir_values_obj = self.env['ir.values']

        ir_values_obj.set_default('purchase.order', 'show_delivery_date', self.default_show_delivery_date)
        ir_values_obj.set_default('purchase.order', 'use_calendar_week', self.default_use_calendar_week)

    def get_default_values(self, fields):
        ir_values_obj = self.env['ir.values']

        show_delivery_date = ir_values_obj.get_default('purchase.order', 'show_delivery_date')
        use_calendar_week = ir_values_obj.get_default('purchase.order', 'use_calendar_week')

        return {
            'default_show_delivery_date': show_delivery_date,
            'default_use_calendar_week': use_calendar_week,
        }


    default_show_delivery_date = fields.Boolean(string='Show the Delivery Date on the Purchase Order [equitania]',
                                                 help='The delivery date will be shown in the Purchase Order',
                                                 default_model='purchase.order')
    default_use_calendar_week = fields.Boolean('Show Calendar Week for Delivery Date [equitania]',
                                                help='The delivery date will be shown as a calendar week',
                                                default_model='purchase.order')
