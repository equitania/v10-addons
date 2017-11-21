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

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)


def log(*args):
    """
        Kleine Hilfsfunktion, die wir als Logger in der Konsole verwenden
    """
    print '#>', args

class res_partner(models.Model):
    _inherit = 'res.partner'

    def _sale_quotation_count(self):
        # The current user may not have access rights for sale orders
        for partner in self:
            partner.eq_sale_quotation_count = len(partner.sale_order_ids.filtered(lambda record: record.state in ('draft', 'sent', 'cancel'))) + len(partner.mapped('child_ids.sale_order_ids').filtered(lambda record: record.state in ('draft', 'sent', 'cancel')))
            partner.sale_order_count = len(partner.sale_order_ids.filtered(lambda record: record.state not in ('draft', 'sent', 'cancel'))) + len(partner.mapped('child_ids.sale_order_ids').filtered(lambda record: record.state not in ('draft', 'sent', 'cancel')))

    def default_user_id(self):
        """
        Setzen des Feldes Verkäufers für einen Partner. Wir automatisch auf Ersteller gesetzt, falls diese Option in den Verkaufseinstellungen aktiviert wurde.
        :return:
        """
        user_id = False
        ir_values_obj = self.env['ir.values']
        creator = ir_values_obj.get_default('res.partner', 'default_creator_saleperson')
        if creator:
            user_id = self._uid
        return user_id

    user_id = fields.Many2one('res.users', string='Salesperson',
      help='The internal user that is in charge of communicating with this contact if any.', default=default_user_id)


    eq_sale_quotation_count = fields.Integer(compute="_sale_quotation_count", string='# of Quotations')
    sale_order_count = fields.Integer(compute="_sale_quotation_count", string='# of Orders')
    eq_delivery_condition_id = fields.Many2one('eq.delivery.conditions', 'Delivery Condition')
    eq_delivery_date_type_sale = fields.Selection([('cw', 'Calendar week'), ('date', 'Date')],
                                                  string="Delivery Date Sale",
                                                  help="If nothing is selected, the default from the settings will be used.")

    # @api.multi
    def name_get(self):
        """
        Überschreiben der name_get-Methode für angepasste Anzeige in Suchboxen
        :return:
        """

        res = []
        tmp_context = self._context
        if not tmp_context:
            tmp_context = {}

        for record in self:
            name = record.name or ''
            if record.parent_id and not record.is_company:
                name = "%s, %s" % (record.parent_id.name, name)
                if record.type == 'contact':
                    name = "%s, %s %s %s" % (record.parent_id.name, (record.title.name if record.title else ''), (record.eq_firstname or ''), record.name or '')
            if not record.parent_id and not record.is_company:
                name = "%s %s %s" % ((record.title.name if record.title else ''), (record.eq_firstname or ''), record.name or '')
            if tmp_context.get('show_address_only'):
                name = self._display_address(without_company=True) # record
            if tmp_context.get('show_address'):
                # TODO - führt zu einem Fehler - Expected singleton: res.partner
                #name = name + "\n" + self._display_address(record, without_company = True)  # record
                name = name + "\n" + self._eq_display_address(record, without_company=True)
                #log(name)

            #name = name.replace('\n\n','\n')
            #name = name.replace('\n\n','\n')
            if tmp_context.get('show_email') and record.email:
                name = "%s <%s>" % (name, record.email)
            res.append((record.id, name))
        return res


    @api.multi
    def _eq_display_address(self, record, without_company = False):
        '''
        The purpose of this function is to build and return an address formatted accordingly to the
        standards of the country where it belongs.

        :param address: browse record of the res.partner to format
        :returns: the address formatted in a display that fit its country habits (or the default ones
            if not country is specified)
        :rtype: string
        '''
        # get the information that will be injected into the display format
        # get the address format
        self = record
        address_format = self.country_id.address_format or \
                         "%(street)s\n%(street2)s\n%(city)s %(state_code)s %(zip)s\n%(country_name)s"
        args = {
            'state_code': self.state_id.code or '',
            'state_name': self.state_id.name or '',
            'country_code': self.country_id.code or '',
            'country_name': self.country_id.name or '',
            'company_name': self.commercial_company_name or '',
        }
        for field in self._address_fields():
            args[field] = getattr(self, field) or ''
        if without_company:
            args['company_name'] = ''
        elif self.commercial_company_name:
            address_format = '%(company_name)s\n' + address_format

        # Erweiterung der Adresse um HausNr.
        address_format = address_format.replace('%(street)s', '%(street)s %(eq_house_no)s')
        #print "* address_format: ", address_format
        #print "------------------------------"
        return address_format % args

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """
        Überschrieben für Anpassung der Anzeige bei der Suche nach einem res_partner
        :param name:
        :param args:
        :param operator:
        :param limit:
        :return:
        """
        ir_values_obj = self.env['ir.values']

        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            # Todo: parent_ids ermitteln
            name = name.split(' / ')[-1]

            argsParents = ['|', '|', '|', ('eq_firstname', operator, name), ('name', operator, name),
                           ('cust_auto_ref', 'ilike', name), ('supp_auto_ref', 'ilike', name)] + args
            # Erweiterung für Suche in Chancen
            resParents = self.search(argsParents, limit=limit)
            if (resParents and resParents.ids):
                args = ['|', '|', '|', '|', ('parent_id', 'in', resParents.ids), ('eq_firstname', operator, name),
                        ('name', operator, name), ('cust_auto_ref', 'ilike', name),
                        ('supp_auto_ref', 'ilike', name)] + args
            else:
                args = ['|', '|', '|', ('eq_firstname', operator, name), ('name', operator, name),
                        ('cust_auto_ref', 'ilike', name), ('supp_auto_ref', 'ilike', name)] + args
        if ir_values_obj.get_default('sale.order', 'default_search_only_company'):
            if self.env.context.has_key('main_address'):
                args += [('is_company', '=', True)]
            elif self.env.context.has_key('default_type'):
                if self.env.context['default_type'] in ['delivery', 'invoice']:
                    args += [('type', '!=', 'contact')]
        elif self.env.context.get('active_model', False) == 'sale.order':
            args = [x for x in args if 'is_company' not in x]
        partner_search = self.search(args, limit=limit)
        res = partner_search.name_get()
        # IDs ermitteln und erneute Suche

        if self.env.context is None:
            self.env.context = {}
        if self.env.context.has_key('active_model'):
            partner_ids = [r[0] for r in res]
            new_res = []

            show_address = ir_values_obj.get_default('sale.order', 'default_show_address')

            for partner_id in self.browse(partner_ids):
                # Company name
                company_name = partner_id.parent_id and partner_id.parent_id.name + ' ; ' or ''
                # Street City
                street = partner_id.street or ''
                house_no = partner_id.eq_house_no or ''
                city = partner_id.city or ''
                partner_name = partner_id.name or ''
                # customer/creditor number
                deb_num = ''
                if partner_id.customer_number != 'False' and partner_id.customer_number and partner_id.supplier_number != 'False' and partner_id.supplier_number:
                    deb_num = '[' + partner_id.customer_number + '/' + partner_id.supplier_number + '] '
                elif partner_id.customer_number != 'False' and partner_id.customer_number:
                    deb_num = '[' + partner_id.customer_number + '] '
                elif partner_id.supplier_number != 'False' and partner_id.supplier_number:
                    deb_num = '[' + partner_id.supplier_number + '] '
                if partner_id.is_company:
                    if show_address:
                        new_res.append((partner_id.id, deb_num + company_name + partner_name + ' / ' + _(
                            'Company') + ' // ' + street + ' ' + house_no + ', ' + city))
                    else:
                        new_res.append((partner_id.id, deb_num + company_name + partner_name + ' / ' + _('Company')))

                else:
                    type = partner_id.type
                    if partner_id.type == 'contact':
                        type = _('contact')
                    elif partner_id.type == 'invoice':
                        type = _('invoice')
                    elif partner_id.type == 'delivery':
                        type = _('delivery')
                    elif partner_id.type == 'default':
                        type = _('default')
                    elif partner_id.type == 'other':
                        type = _('other')
                    if show_address:
                        new_res.append((partner_id.id, "%s %s %s %s" % (
                        deb_num + company_name, (partner_id.title.name if partner_id.title else ''),
                        (partner_id.eq_firstname if partner_id.eq_firstname else ''),
                        (partner_id.name or '') + ' / ' + type + ' // ' + street + ' ' + house_no + ', ' + city)))
                    else:
                        new_res.append((partner_id.id, "%s %s %s %s" % (
                        deb_num + company_name, (partner_id.title.name if partner_id.title else ''),
                        (partner_id.eq_firstname if partner_id.eq_firstname else ''), partner_name + ' / ' + type)))
            return new_res
        return res


class eq_partner_extension_base_config_settings(models.TransientModel):
    _inherit = "sale.config.settings"

    def set_default_creator(self):
        ir_values_obj = self.env['ir.values']
        ir_values_obj.set_default('res.partner', 'default_creator_saleperson', self.default_creator_saleperson or False)

    def get_default_creator(self, fields):
        ir_values_obj = self.env['ir.values']
        creator = ir_values_obj.get_default('res.partner', 'default_creator_saleperson')
        return {
            'default_creator_saleperson': creator,
        }

    # def set_default_reset_password(self, cr, uid, ids, context):
    #     ir_values_obj = self.pool.get('ir.values')
    #     config = self.browse(cr, uid, ids[0], context)
    #
    #     ir_values_obj.set_default(cr, uid, 'res.users', 'default_reset_passwort',
    #                               config.default_reset_passwort or False)
    #
    # def get_default_reset_password(self, cr, uid, ids, context):
    #     ir_values_obj = self.pool.get('ir.values')
    #     reset = ir_values_obj.get_default(cr, uid, 'res.users', 'default_reset_passwort')
    #     return {
    #         'default_reset_passwort': reset,
    #     }

    default_creator_saleperson = fields.Boolean('The creator of the address dataset will be set automatically as sales person. [eq_sale]')

