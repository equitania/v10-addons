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

from openerp import models, fields, api
import json
import eq_ebid_services
from openerp.osv import osv


class eq_ebid_protocol(models.Model):
    """
    Protokollierung der Ergebnisse des Datenabgleichs
    """

    _name = "eq.ebid.protocol"
    _rec_name = 'eq_partner_name'
    _description = ""
    
    # eq_res_id = fields.Integer("Adresse ID", required=True)
    eq_res_id = fields.Many2one('res.partner', string='Address', required=True)
    # 'eq_customer_id': fields.many2one('res.partner', 'Customer', required=True),
    # eq_customer_name = fields.related('eq_customer_id', 'name', type='char', size=128, readonly=True)
    
    eq_model = fields.Char("Model")
    eq_request = fields.Text(string="Request", help="Request")
    eq_response = fields.Text(string="Response", help="Response")
    eq_message = fields.Text(string="Message", help="Message")
    eq_rate = fields.Integer("Seach rate")
    eq_checked = fields.Boolean("Result checked")
    eq_result_count = fields.Integer("Result count")
    eq_request_type = fields.Integer("Request type")
    
    eq_protocol_positions = fields.One2many('eq.ebid.protocol.position', 'eq_ebid_protocol_id', string='EBID Protocol', readonly=True)
    
    eq_partner_name = fields.Char(string="Name", compute='compute_request_params')
    
    eq_request_street = fields.Char(string="Street", compute='compute_request_params')
    eq_request_zip = fields.Char(string="Zip", compute='compute_request_params')
    eq_request_city = fields.Char(string="City", compute='compute_request_params')

    def compute_request_params(self):
        """
        Auslesen der Suchparameter aus dem Request
        :return:
        """
        for rec in self:
            if (rec.eq_request_type == 1):  # Suche über Adressdaten
                try:
                    eq_req_des = json.loads(rec.eq_request) 
        
                    rec.eq_partner_name = eq_req_des['companyName']
                    rec.eq_request_street = eq_req_des['street']                    
                    if (('houseno' in eq_req_des) and eq_req_des['houseno']):
                        rec.eq_request_street += ' ' + eq_req_des['houseno']
                        
                    rec.eq_request_zip = eq_req_des['zip']
                    rec.eq_request_city = eq_req_des['city']
                except KeyError:
                    pass

    def eq_create_protocol_entry(self, search_company_result):
        """
        Anlage eines neuen Datensatzes
        :param search_company_result: Ergebnis der Suchanfrage an Unternehmensverzeichnis.org
        :return:
        """
        rate = 0
        result_count = 0
        if search_company_result.searchHits and len(search_company_result.searchHits) > 0:
            rate = search_company_result.searchHits[0].rate
            result_count = len(search_company_result.searchHits)

        data = {
                    'eq_res_id': search_company_result.res_id,
                    'eq_model': search_company_result.model or None,
                    'eq_request': search_company_result.request or None,
                    'eq_response': search_company_result.response or None,
                    'eq_message': search_company_result.error or None,
                    'eq_rate': rate,
                    'eq_request_type': search_company_result.request_type,
                    'eq_result_count': result_count,
                }
        new_obj = self.create(data)
        return new_obj.id

    def eq_update_protocol_entry(self, result):
        if not result:
            return
        
        rate = 0
        result_count = 0
        if result.searchHits and len(result.searchHits) > 0:
            rate = result.searchHits[0].rate
            result_count = len(result.searchHits) 

        data = {
                    'eq_request': result.request or None,
                    'eq_response':  result.response or None,
                    'eq_message': result.error or None,
                    'eq_rate': rate,
                    'eq_request_type': result.request_type,
                    'eq_result_count': result_count,
                }
        self.write(data)


class eq_ebid_protocol_position(models.Model):
    """
    Detaileinträge für EBID-Protokolle
    """
    _name = "eq.ebid.protocol.position"
    _rec_name = 'eq_company_name'
    _description = ""
    
    # match request
    ebid_no = fields.Char("EBID-No")
    eq_rate = fields.Integer("Seach rate")
    
    # company request
    eq_company_name = fields.Char("Company name")
    eq_street = fields.Char("Street")
    eq_house_no = fields.Char("House No")
    eq_city = fields.Char("City")
    eq_city_part = fields.Char("City part")
    eq_zip = fields.Char("Zip")
    eq_country = fields.Char("Country")
    eq_phone = fields.Char("Phone")
    eq_fax = fields.Char("Fax")
    eq_mobile = fields.Char("Mobile")
    eq_email = fields.Char("E-Mail")
    eq_url = fields.Char("Homepage")
    eq_ustid_nr = fields.Char("UstidNr")
  
    eq_ebid_protocol_id = fields.Many2one('eq.ebid.protocol', string='Parent Protocol', ondelete='cascade', required=True)
    
    eq_response = fields.Text(string="Response", help="Response")
    
    @api.multi
    def open_url_for_ebid(self, args=None):
        """
        Button "Zu Unternehmensverzeichnis.org springen"
        :param args:
        :return:
        """
        ebid_settings = eq_ebid_services.get_ebid_settings(self)
        if (not ebid_settings or not ebid_settings.homepage):
            return
        
        return {
            'type': 'ir.actions.act_url',
            'url': ebid_settings.homepage + self.ebid_no,
            'target': 'new',
        }
        
    @api.multi   
    def get_data_for_ebid_no(self, args=None):
        """
        Button "Adressdaten aus Unternehmensverzeichnis.org laden"
        :param args:
        :return:
        """
        settings = eq_ebid_services.get_ebid_settings(self)
        
        if (not eq_ebid_services.settings_ok(settings)):
            raise osv.except_osv(_('Error'), _('Check the configuration for EBID'))
        
        search_res = eq_ebid_services.get_company_for_ebid(self.eq_ebid_protocol_id.eq_res_id.id, self.ebid_no, settings)
        result = search_res.ebid_search_result
        
        if (not search_res.requestOK):
            update_vals = {
                            'eq_response': search_res.response,
                           }
            self.write(update_vals)
        
        # update für Position
        if (result):
            update_vals = {
                            'eq_company_name': result.company_name,
                            'eq_street': result.street or None,
                            'eq_house_no': result.house_no or None,
                            'eq_city':  result.city or None,
                            'eq_city_part': result.city_part or None,
                            'eq_zip': result.zip,
                            'eq_country': result.country,
                            'eq_phone': result.phone,
                            'eq_fax': result.fax,
                            'eq_email': result.email,
                            'eq_mobile': result.mobile,
                            'eq_url': result.url,
                            'eq_ustid_nr': result.ustid_nr,
                           }
            self.write(update_vals)
        return
    
    @api.multi
    def set_ebid_no_for_partner(self, args=None):
        """
        Button "EBID-Nummer für Adresse setzen"
        :param args:
        :return:
        """
        if (not self.ebid_no):
            return
        
        partner_obj = self.env['res.partner']
        partner_id = self.eq_ebid_protocol_id.eq_res_id.id
        if (partner_id and partner_id > 0):
            found_partner = partner_obj.browse(partner_id)
            if (found_partner):
                update_vals = {
                               'eq_ebid_was_checked': True,
                               'eq_ebid_no': self.ebid_no
                               }
                found_partner[0].write(update_vals)
  
    @api.multi
    def set_ebid_data_for_partner(self, args=None):
        """
        Button "Daten in Adresse übernehmen"
        Übernahme der Daten aus Unternehmensverzeichnis.org
        :param args:
        :return:
        """
        if (not self.ebid_no):
            return
        
        partner_obj = self.env['res.partner']
        partner_id = self.eq_ebid_protocol_id.eq_res_id.id
        if (partner_id and partner_id > 0):
            found_partner = partner_obj.browse(partner_id)
            if (found_partner):
                street = self.eq_street
                # if (self.eq_house_no):
                #    street += ' ' + self.eq_house_no #später in eigenes Feld
                update_vals = {
                               'eq_ebid_was_checked': True,
                               'eq_ebid_no': self.ebid_no,
                               'name': self.eq_company_name,
                               'street': street,
                               'eq_house_no': self.eq_house_no,
                               'zip': self.eq_zip,
                               'city': self.eq_city,
                               'eq_city_part': self.eq_city_part,
                               'phone': self.eq_phone,
                               'mobile': self.eq_mobile,
                               'email': self.eq_email,
                               'fax': self.eq_fax,
                               'website': self.eq_url,
                               'vat': self.eq_ustid_nr
                               }
                found_partner[0].write(update_vals)            

    @api.multi
    def write_date_from_ebid(self, args=None):
        return
    
    def create_position_for_company_search(self, parent_id, result):
        """
        Neue Detailposition für einen Protokolleintrag nach einer Firmensuche
        :param parent_id:
        :param result:
        :return:
        """
        if (not result):
            return
        
        data = {
               # 'eq_res_id': result.res_id,
               # 'eq_model': result.model or None,
                'ebid_no': result.ebid_no,
                # 'eq_request': result.request or None,
                'eq_response':  result.arr_rate or None,
                # 'eq_message': result.error or None,
                'eq_rate': result.rate,
                'eq_ebid_protocol_id': parent_id
            }
        self.create(data)
        
    def update_position_for_company_search(self, result):
        if(result):
            data = {
                    'ebid_no': result.ebid_no,
                    'eq_response':  result.arr_rate or None,
                    'eq_rate': result.rate,
                }
            self.write(data)
        
    def update_position_for_ebid_search(self, result):
        if (not result):
            return
        
        data = {
                'ebid_no': result.ebid_no,
                'eq_company_name': result.company_name,
                'eq_street': result.street or None,
                'eq_house_no': result.house_no or None,
                'eq_city':  result.city or None,
                'eq_city_part': result.city_part or None,
                'eq_zip': result.zip,
                'eq_country': result.country,
                'eq_phone': result.phone,
                'eq_fax': result.fax,
                'eq_email': result.email,
                'eq_mobile': result.mobile,
                'eq_url': result.url,
                'eq_ustid_nr': result.ustid_nr,
            }
        self.write(data)   
        
    def create_position_for_ebid_search(self, parent_id, result):
        """
        Neue Detailposition für einen Protokolleintrag nach einem Abgleich über die EBID
        :param parent_id:
        :param result:
        :return:
        """
        if (not result):
            return
        
        data = {
                'ebid_no': result.ebid_no,
                'eq_company_name': result.company_name,
                'eq_street': result.street or None,
                'eq_house_no': result.house_no or None,
                'eq_city':  result.city or None,
                'eq_city_part': result.city_part or None,
                'eq_zip': result.zip,
                'eq_country': result.country,
                'eq_phone': result.phone,
                'eq_fax': result.fax,
                'eq_email': result.email,
                'eq_mobile': result.mobile,
                'eq_url': result.url,
                'eq_ustid_nr': result.ustid_nr,
                'eq_ebid_protocol_id': parent_id,
            }
        self.create(data)   
