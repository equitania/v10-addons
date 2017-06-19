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



class eq_partner_sale_order_extension(models.Model):
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


    eq_invoice_address = fields.Char(compute='_compute_invoice_address', string=" ", store=False)
    eq_delivery_address = fields.Char(compute='_compute_delivery_address', string=" ", store=False)
    client_order_ref = fields.Char('Reference/Description', copy=True) # Standard: copy = False
    eq_street_house_no = fields.Char(compute='_compute_street_house_no', string=" ", store=False)
    eq_zip_city = fields.Char(compute='_compute_zip_city', string=" ", store=False)
    eq_country = fields.Char(compute='_compute_country', string=" ", store=False)
