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
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as OE_DFORMAT



class eq_sale_order_extension(models.Model):
    _inherit = 'sale.order'


    eq_delivery_condition_id = fields.Many2one('eq.delivery.conditions', 'Delivery Condition')
        # 'partner_id': fields.many2one('res.partner', 'Customer', readonly=True,
        #                               states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        #                               required=True, change_default=True, select=True, track_visibility='always'),



    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """
        Override für Wechsel der Partner_ID: Übernahme der custom-Felder
        Umfang noch abzuklären (eq_incoterm; VEP-25)
        :return:
        """

        super(eq_partner_sale_order_extension, self).onchange_partner_id()

        partner = self.partner_id
        if partner:
            # if partner.eq_incoterm:
            #     self.incoterm = partner.eq_incoterm.id
            # else:
            #     self.incoterm = False

            if partner.eq_delivery_condition_id:
                self.eq_delivery_condition_id = partner.eq_delivery_condition_id.id
            else:
                self.eq_delivery_condition_id = False

            self.client_order_ref = partner.eq_foreign_ref

            # if partner.eq_default_delivery_address:
            #     self.partner_shipping_id = partner.eq_default_delivery_address.id
            # if partner.eq_default_invoice_address:
            #     self.partner_invoice_id = partner.eq_default_invoice_address.id

    @api.multi
    def _compute_street_house_no(self):
        """ Generate street and house no info for sale order """

        for sale_order in self:
            computed_street_house_no = ''
            if sale_order.partner_id.street and sale_order.partner_id.eq_house_no:
                computed_street_house_no = sale_order.partner_id.street + ' ' + sale_order.partner_id.eq_house_no
            elif sale_order.partner_id.street:
                computed_street_house_no = sale_order.partner_id.street

            sale_order.eq_street_house_no = computed_street_house_no

    @api.multi
    def _compute_zip_city(self):
        """ Generate zip and city info for sale order (eq_zip_city) """

        for sale_order in self:
            zip_city = ''
            if sale_order.partner_id:
                if sale_order.partner_id.zip and sale_order.partner_id.city:
                    zip_city = sale_order.partner_id.zip + ' ' + sale_order.partner_id.city
                elif sale_order.partner_id.zip:
                    zip_city = sale_order.partner_id.zip
                elif sale_order.partner_id.city:
                    zip_city = sale_order.partner_id.city
            sale_order.eq_zip_city = zip_city


    @api.multi
    def _compute_country(self):
        """ Generate country info for sale order (eq_country) """

        for sale_order in self:
            if sale_order.partner_id and sale_order.partner_id.country_id:
                sale_order.eq_country = sale_order.partner_id.country_id.name
            else:
                sale_order.eq_country = ''


    @api.multi
    def _compute_invoice_address(self):
        """ Generate address infos for sale order (eq_invoice_address) """

        for sale_order in self:
            computed_address = ''
            zip = ""
            if sale_order.partner_shipping_id.zip:
                zip = sale_order.partner_shipping_id.zip

            if sale_order.partner_invoice_id:
                if sale_order.partner_invoice_id.street and sale_order.partner_invoice_id.city:
                    if sale_order.partner_invoice_id.eq_house_no:
                        computed_address = sale_order.partner_invoice_id.street + ' ' + sale_order.partner_invoice_id.eq_house_no + ', @ZIP ' + sale_order.partner_invoice_id.city
                    else:
                        computed_address = sale_order.partner_invoice_id.street + ', @ZIP ' + sale_order.partner_invoice_id.city
                elif sale_order.partner_invoice_id.street:
                    if sale_order.partner_invoice_id.eq_house_no:
                        computed_address = sale_order.partner_invoice_id.street + ' ' + sale_order.partner_invoice_id.eq_house_no
                    else:
                        computed_address = sale_order.partner_invoice_id.street
                elif sale_order.partner_invoice_id.city:
                    computed_address= sale_order.partner_invoice_id.city

            if computed_address:
                computed_address = computed_address.replace("@ZIP", zip)

            sale_order.eq_invoice_address = computed_address




    @api.multi
    def _compute_delivery_address(self):
        """ Generate address infos for sale order (eq_delivery_address)"""

        for sale_order in self:
            zip = ""
            sale_order.eq_delivery_address = ''
            if sale_order.partner_shipping_id.zip:
                zip = sale_order.partner_shipping_id.zip

            if sale_order.partner_shipping_id.street and sale_order.partner_shipping_id.city:
                if sale_order.partner_shipping_id.eq_house_no:
                    sale_order.eq_delivery_address = sale_order.partner_shipping_id.street + ' ' + sale_order.partner_shipping_id.eq_house_no + ', @ZIP ' + sale_order.partner_shipping_id.city
                else:
                    sale_order.eq_delivery_address = sale_order.partner_shipping_id.street + ', @ZIP ' + sale_order.partner_shipping_id.city
            elif sale_order.partner_shipping_id.street:
                if sale_order.partner_shipping_id.eq_house_no:
                    sale_order.eq_delivery_address = sale_order.partner_shipping_id.street + ' ' + sale_order.partner_shipping_id.eq_house_no
                else:
                    sale_order.eq_delivery_address = sale_order.partner_shipping_id.street
            elif sale_order.partner_shipping_id.city:
                sale_order.eq_delivery_address = sale_order.partner_shipping_id.city

            if sale_order.eq_delivery_address:
                result = sale_order.eq_delivery_address
                result = result.replace("@ZIP", zip)
                sale_order.eq_delivery_address = result

    @api.multi
    def _prepare_invoice(self):
        """
        Überschrieben für Übernahme von Kopf- und Fußtext in die Rechnung
        :return:
        """

        result = super(eq_sale_order_extension, self)._prepare_invoice()
        result['eq_head_text'] = self.eq_head_text
        result['comment'] = self.note
        return result


    eq_invoice_address = fields.Char(compute='_compute_invoice_address', string=" ", store=False)
    eq_delivery_address = fields.Char(compute='_compute_delivery_address', string=" ", store=False)
    client_order_ref = fields.Char('Reference/Description', copy=True) # Standard: copy = False
    eq_street_house_no = fields.Char(compute='_compute_street_house_no', string=" ", store=False)
    eq_zip_city = fields.Char(compute='_compute_zip_city', string=" ", store=False)
    eq_country = fields.Char(compute='_compute_country', string=" ", store=False)

    eq_head_text = fields.Html(string="Header", translate=True)
    note = fields.Html('Terms and conditions') # überschrieben als HTML-Feld

    # Report
    show_delivery_date = fields.Boolean(string='Show Delivery Date')
    use_calendar_week = fields.Boolean('Use Calendar Week for Delivery Date[equitania]')


class eq_sale_configuration_address(models.TransientModel):
    _inherit = 'sale.config.settings'
    # _inherit = _name

    def set_default_values(self):
        ir_values_obj = self.env['ir.values']

        ir_values_obj.set_default('sale.order', 'default_show_address', self.default_show_address or False)
        ir_values_obj.set_default('sale.order', 'default_search_only_company', self.default_search_only_company or False)
        ir_values_obj.set_default('sale.order', 'show_delivery_date', self.default_show_delivery_date)
        ir_values_obj.set_default('sale.order', 'use_calendar_week', self.default_use_calendar_week)
        ir_values_obj.set_default('sale.order.line', 'eq_use_internal_description', self.default_eq_use_internal_description)

    def get_default_values(self, fields):
        ir_values_obj = self.env['ir.values']
        notification = ir_values_obj.get_default('sale.order', 'default_show_address')
        only_company = ir_values_obj.get_default('sale.order', 'default_search_only_company')
        show_delivery_date = ir_values_obj.get_default('sale.order', 'show_delivery_date')
        use_calendar_week = ir_values_obj.get_default('sale.order', 'use_calendar_week')
        eq_use_internal_description = ir_values_obj.get_default('sale.order.line', 'eq_use_internal_description')
        return {
            'default_show_address': notification,
            'default_search_only_company': only_company,
            'default_show_delivery_date': show_delivery_date,
            'default_use_calendar_week': use_calendar_week,
            'default_eq_use_internal_description': eq_use_internal_description,
        }

    default_show_address = fields.Boolean(
            string='Show street and city in the partner search of the Sale and Purchase Order [equitania]',
            help="This adds the street and the city to the results of the partner search of the Sale and Purchase Order.")
    default_search_only_company = fields.Boolean(string='Only Search for Companies [equitania]',
                                                      help="Only Companies will be shown in the Customer search of the Sale and Purchase Order.")
    group_product_rrp = fields.Boolean(string='Show RRP for products [equitania]', implied_group='eq_sale.group_product_rrp')
    default_show_delivery_date = fields.Boolean(string='Show the Delivery Date on the Sale Order [equitania]',
                                                 help='The delivery date will be shown in the Sale Order',
                                                 default_model='sale.order')
    default_use_calendar_week = fields.Boolean('Show Calendar Week for Delivery Date [equitania]',
                                                help='The delivery date will be shown as a calendar week',
                                                default_model='sale.order')
    default_eq_use_internal_description = fields.Boolean('Use internal description for sale orders [equitania]',
                                                          help='The internal description will be used for sale orders not the sale description',
                                                          default_model='sale.order.line')


class eq_sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _get_delivery_date(self):
        """
        Hilfsfunktion für Report für Ermittlung des Lieferdatums
        Aktuell wird Feld show_delivery_date der sale_order nicht gesetzt -> Rückgabe immer false
        :return:
        """
        result = {}
        for order_line in self:
            if order_line.order_id.show_delivery_date and order_line.eq_delivery_date:
                delivery_date = datetime.strptime(order_line.eq_delivery_date, OE_DFORMAT)
                if order_line.order_id.partner_id.eq_delivery_date_type_sale:
                    if order_line.order_id.partner_id.eq_delivery_date_type_sale == 'cw':
                        result[order_line.id] = 'KW ' + delivery_date.strftime('%V/%Y')
                    elif order_line.order_id.partner_id.eq_delivery_date_type_sale == 'date':
                        result[order_line.id] = delivery_date.strftime('%d.%m.%Y')
                else:
                    if order_line.order_id.use_calendar_week:
                        result[order_line.id] = 'KW ' + delivery_date.strftime('%V/%Y')
                    else:
                        result[order_line.id] = delivery_date.strftime('%d.%m.%Y')
            else:
                result[order_line.id] = False
        return result


    # ODOO 10: Feld delay fehlt für sale_order_line
    # @api.onchange('eq_delivery_date')
    # def on_change_delivery_date(self):
    #     """
    #
    #     :return:
    #     """
    #
    #     date_order = self.order_id.date_order if self.order_id else False
    #     if date_order and self.eq_delivery_date:
    #         date_order = datetime.strptime(date_order.split(' ')[0], OE_DFORMAT)
    #         eq_delivery_date = datetime.strptime(eq_delivery_date, OE_DFORMAT)
    #
    #         self.delay = (eq_delivery_date - date_order).days




    def generate_line_text_with_attributes(self, attributes, product_id, eq_use_internal_description):
        """
        ! WICHTIG ! - jede Änderung dieser Funktion muss man auch gleich im odoo-website\eq_website_customerportal\eq_website_sale_sale_order.py machen !

        Erstellt den Text einer Bestellposition und verwendet dabei den Verkaufstext zusammen mit dem Text aus den Varianten (immer als [Attributwert]: [Attributtext])
        @param attributes: Attribute, die bei eine Variante gesetzt sind
        @param product_id: ID der Produktvariante
        @param eq_use_internal_description: True -> wir soll das Feld Beschreibung von Template verwenden
        @return: Bestellposition mit kompletten Text
        """

        attribute_info_list = []
        for attribute in attributes:
            attribute_info = attribute.attribute_id.name + ": " + attribute.name
            attribute_info_list.append(attribute_info)

        attribute_string = "\n".join(attribute_info_list)

        # if name is False:                   # name is set, don't reset it again !
        if not eq_use_internal_description and product_id.description_sale:
            if product_id.description_sale.strip() == '' or product_id.description_sale == None:
                result = attribute_string
            else:
                result = product_id.description_sale + "\n" + attribute_string
        elif eq_use_internal_description and product_id.description:
            result = product_id.product_tmpl_id.description + "\n" + attribute_string
        else:
            # falls kein Verkaufstext bei dem Produkt ist und Variante einen Text hat, soll man den Text der Variante ausgeben - z.B. Farbe: Rot, Blau
            if attribute_string:
                """
                wenn kein Verkaufstext bei dem Produkt hinterlegt ist, müssen wir es so machen sonst wird der Text mit dem Attribut + Attributwert
                wegen der Defaultdefinition im Kern nicht angezeigt.
                Hier ist es:
                <div class="text-muted" t-esc="'\n'.join(line.name.splitlines()[1:])"/>
                """

                # result = "\n" + attribute_string
                # Anpassung für Ticket 4086: unnötige Leerzeile vermeiden
                result = attribute_string
            else:
                result = ' '

        return result


    @api.onchange('product_id')
    def product_id_change(self):
        """
            Setzen des Namensfeldes für eine Auftragsposition beim Wechsel des Produkts
        """
        vals = super(eq_sale_order_line, self).product_id_change()

        qty = self.product_uom_qty

        # Creates new dict for if not present and sets the customer language. The frozendict context can't be edited.
        context_new = {}
        if self._context:
            context_new = dict(self._context)

        context_new['lang'] = self.env['res.partner'].browse(self.order_id.partner_id.id).lang
        product_id = self.env['product.product'].with_context(context_new).browse(self.product_id.id)

        eq_use_internal_descriptionion = self.env['ir.values'].get_default('sale.order.line', 'eq_use_internal_description')

        # vals['value']['product_uos_qty'] = qty * product_id.uos_coeff

        attributes = product_id.attribute_value_ids

        # set product name only after first change of quantity - it's our workaround for refresh problem after each change of quantity
        if vals.get("value", False):
            vals['value'].pop('name', None)

        if self._context != None and not self._context.get('uom_qty_change', False) and not self._context.get('uos_qty_change', False):
            # Alte Version - Beispiel: Blau, Klein

            # Neue Version - Beispiel: Farbe: Blau, Typ: Klein
            self.name = self.generate_line_text_with_attributes(attributes, product_id, eq_use_internal_descriptionion)

        # vals['value']['delay'] = product_id.sale_delay
        return vals

    eq_delivery_date = fields.Date('Delivery Date')
    get_delivery_date = fields.Char(compute="_get_delivery_date", string="Delivery", methode=True, store=False)
    eq_use_internal_description = fields.Boolean('Use internal description for sale orders')