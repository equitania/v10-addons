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

from openerp import models, fields, api, _
import eq_ebid_services
from openerp import SUPERUSER_ID
from openerp.osv import osv
from __builtin__ import str

import logging
_logger = logging.getLogger(__name__)


class eq_partner_ebid(models.Model):
    _inherit = ['res.partner']
    
    eq_ebid_no = fields.Char(string="EBID Number", size=15)
    eq_ebid_was_checked = fields.Boolean('EBID-Suche wurde durchgeführt')

    def get_ebid_settings(self):
        """         
            Get the ebid settings
        """

        config_params = self.env['ir.config_parameter']
        match_url = config_params.get_param("eq.ebid.service.match.url",False)
        company_url = config_params.get_param("eq.ebid.service.company.url",False)
        search_url = config_params.get_param("eq.ebid.service.search.url", False)
        homepage_url = config_params.get_param("eq.ebid.homepage.url",False)
        logging_active_conf_val = config_params.get_param("eq.ebid.activate.log", False)

        if logging_active_conf_val:
            activate_log = True if (logging_active_conf_val == 'True' or logging_active_conf_val == 'true') else False
        else:
            activate_log = False

        if (company_url and not company_url.endswith('/')):
            company_url += '/'
        if (homepage_url and not homepage_url.endswith('/')):
            homepage_url += '/'
        if (search_url and not search_url.endswith('/')):
            search_url += '/'
        
        user = config_params.get_param("eq.ebid.user",False)
        pw = config_params.get_param("eq.ebid.pw",False)
        rate_txt = config_params.get_param("eq.ebid.acceptance.rate",False)

        rate = 90
        if (rate_txt):
            rate = int(rate_txt)
        settings = eq_ebid_services.EbidSettings(user, pw, match_url, company_url, search_url, homepage_url, activate_log, rate)
        return settings
    
    def settings_ok(self, ebid_settings):
        return ebid_settings.user and ebid_settings.pw and ebid_settings.urlMatch 

    def get_chunks(self, l, n):
        for i in xrange(0, len(l), n):
            yield l[i:i+n]

    def eq_check_ebid_cron(self, ebid_search_mode=False, limit=0, check_interval=0):
        """
        Funktion des Cronjobs zur Überprüfung der Adressdatensätze
        :param ebid_search_mode: True: Kontrolle der Datensätze mit existierenden EBIDs
        :param limit:
        :param check_interval: Anzahl der Tage seit der letzten Überprüfung
        :return:
        """
        if (ebid_search_mode):
            # Kontrolle der Daten, für die die EBID-Nr gesetzt ist und für die der letzte Protokolleintrag mehr als
            # der Wert für check_interval in Tagen zurückliegt
            if (check_interval <= 0):
                check_interval = 1
            interval_text = "'" + str(check_interval) + " day'"

            sql_select = """SELECT p.ID FROM res_partner p INNER JOIN eq_ebid_protocol prot on prot.eq_res_id = p.id WHERE 
                            (coalesce(p.eq_ebid_no, '') <> '') AND (prot.write_date < (CURRENT_TIMESTAMP - INTERVAL """ + interval_text + """)) ORDER BY prot.write_date"""

            if ((limit > 0) and (isinstance(limit, int))):
                sql_select += ' limit ' + str(limit)

            self._cr.execute(sql_select)
            partner_ids = [x[0] for x in self._cr.fetchall()]

            if (partner_ids):
                chunks = self.get_chunks(partner_ids, 200)
                for list_part in chunks:
                    check_partner = self.browse(list_part)
                    if (check_partner):
                        check_partner.get_company_data_for_ebid()

            """ alt
            search_filter = [('eq_ebid_no','!=', False)]
            if (plz_filter):
                search_filter.append(('zip','=like', str(plz_filter) + '%'))

            check_partner_ids = self.search(cr, SUPERUSER_ID, search_filter)

            if (check_partner_ids):
                chunks = self.get_chunks(check_partner_ids, 200)
                for list_part in chunks:
                    check_partner = self.browse(cr,SUPERUSER_ID,list_part,context)
                    if (check_partner):
                        check_partner.get_company_data_for_ebid()
            """
        else:
            # Abarbeitung der Datensätze, für die noch keine EBID-Nr gesetzt wurde
            sql_select = "SELECT p.ID FROM res_partner p LEFT OUTER JOIN eq_ebid_protocol prot on prot.eq_res_id = p.id WHERE p.is_company AND (coalesce(p.eq_ebid_no,'') = '') AND prot.id is null"
            if ((limit > 0) and (isinstance(limit, int))):
                sql_select += ' limit ' + str(limit)

            self._cr.execute(sql_select)
            partner_ids = [x[0] for x in self._cr.fetchall()]

            # search_filter = [('eq_ebid_no','=',False), ('is_company','=', True)]
            # if (plz_filter):
            #   search_filter.append(('zip','=like', str(plz_filter) + '%'))

            # alt
            # check_partner_ids = self.search(cr, SUPERUSER_ID, search_filter)

            if (partner_ids):
                chunks = self.get_chunks(partner_ids, 200)
                for list_part in chunks:
                    partners_for_search = self.browse(list_part)
                    partners_for_search.search_ebid()

    @api.multi
    def show_data_for_ebid(self, args = None):
        """
        Öffnen der Seite für die Adresse im Unternehmensverzeichnis
        :param args:
        :return:
        """
        if (not self.eq_ebid_no):
            return
        
        ebid_settings = self.get_ebid_settings()
        if (not ebid_settings and not ebid_settings.homepage):
            return
         
        return {
            'type': 'ir.actions.act_url',
            'url': ebid_settings.homepage + self.eq_ebid_no,
            'target': 'new',
        }
        
    @api.multi
    def get_company_data_for_ebid(self, args = None):
        """
        Auslesen der Daten aus dem Unternehmensverzeichnis über die EBID
        :param args:
        :return:
        """
        if (not self):
            return
   
        ebid_settings = eq_ebid_services.get_ebid_settings(self[0]);
        
        if (not self[0].settings_ok(ebid_settings)):
            raise osv.except_osv(_('Error'), _('Check the configuration for EBID'))
        
        # eq_ebid_services.check_authentication(ebid_settings)
       
        eq_prot_obj = self[0].env['eq.ebid.protocol']
        eq_prot_position_obj = self[0].env['eq.ebid.protocol.position']
        for partner in self:
            # self.proc_get_ebid_for_address_step(ebid_settings, partner)
            
            found_company = eq_ebid_services.get_company_for_ebid(partner.id, partner.eq_ebid_no, ebid_settings)
            
            protocol_id = 0
            protocol_for_partner = eq_prot_obj.sudo().search([('eq_res_id','=',partner.id), ('eq_model', '=', 'res.partner')])
            if (not protocol_for_partner):
                # create prot
                protocol_id = eq_prot_obj.eq_create_protocol_entry(found_company)
                if (found_company.requestOK and (protocol_id > 0)):
                    eq_prot_position_obj.create_position_for_ebid_search(protocol_id, found_company.ebid_search_result)
                continue
            else:
                protocol_id =  protocol_for_partner.ids[0]
            
            protocol_record = eq_prot_obj.sudo().browse(protocol_for_partner.ids)
            if (protocol_record):
                protocol_record[0].eq_update_protocol_entry(found_company)
                    
            if (not found_company.requestOK):
                continue  # log error
            
            prot_position_ids = eq_prot_position_obj.sudo().search([('eq_ebid_protocol_id','in',protocol_for_partner.ids), ('ebid_no','=',partner.eq_ebid_no)])
            if (not prot_position_ids):
                eq_prot_position_obj.create_position_for_ebid_search(protocol_id, found_company.ebid_search_result)
                continue
            
            prot_pos = eq_prot_position_obj.sudo().browse(prot_position_ids.ids)
            if (prot_pos):
                result= found_company.ebid_search_result
                prot_pos[0].update_position_for_ebid_search(result)  # .write(update_vals)
            
                # Bei Änderungen Flag setzen
            # Update protocols
    """
    def proc_get_company_for_ebid_step(self, ebid_settings, partner):   
        eq_prot_obj = self[0].env['eq.ebid.protocol']
        eq_prot_position_obj = self[0].env['eq.ebid.protocol.position']
    
        found_company = eq_ebid_services.get_company_for_ebid(partner.id, partner.eq_ebid_no, ebid_settings)
        
        protocol_id = 0
        protocol_for_partner = eq_prot_obj.sudo().search([('eq_res_id','=',partner.id), ('eq_model', '=', 'res.partner')])
        if (not protocol_for_partner):
            #create prot
            protocol_id = eq_prot_obj.eq_create_protocol_entry(found_company)
            if (found_company.requestOK and (protocol_id > 0)):
                eq_prot_position_obj.create_position_for_ebid_search(protocol_id, found_company.ebid_search_result)
            return
        else:
            protocol_id =  protocol_for_partner.ids[0]
        
        if (not found_company.requestOK):
            protocol_record = eq_prot_obj.sudo().browse(protocol_for_partner.ids)
            if (protocol_record):
                protocol_record[0].eq_update_protocol_entry(found_company)
            return #log error
        
        prot_position_ids = eq_prot_position_obj.sudo().search([('eq_ebid_protocol_id','in',protocol_for_partner.ids), ('ebid_no','=',partner.eq_ebid_no)])
        if (not prot_position_ids):
            eq_prot_position_obj.create_position_for_ebid_search(protocol_id, found_company.ebid_search_result)
            return
        
        prot_pos = eq_prot_position_obj.sudo().browse(prot_position_ids.ids)
        if (prot_pos):
            result= found_company.ebid_search_result
            prot_pos[0].update_position_for_ebid_search(result)
    """    
    
    @api.multi
    def button_search_ebid(self, args = None):
        """
        Button "Überpfüfen"
        Suche nach der EBID anhand der Adressdaten
        :param args:
        :return:
        """
        ebid_settings = self[0].get_ebid_settings()
       
        if (not self[0].settings_ok(ebid_settings)):
            raise osv.except_osv(_('Error'), _('Check the configuration for EBID'))
        
        req_result = self.proc_search_ebid_for_address(self, ebid_settings, True)
        if (req_result and not req_result.success):
            return self.show_message(_('Search for EBID'), req_result.message, req_result.res_id)
        
    @api.multi
    def search_ebid(self, args=None):
        """
        Ermittlung der EBID-Nummern für die Adressdaten
        (Aufruf durch Cronjob)
        """
        if (not self):
            return
   
        ebid_settings = self[0].get_ebid_settings()
        
        if (not self[0].settings_ok(ebid_settings)):
            raise osv.except_osv(_('Error'), _('Check the configuration for EBID'))
        
        eq_prot_obj = self[0].env['eq.ebid.protocol']
        eq_prot_position_obj = self[0].env['eq.ebid.protocol.position']
        for partner in self:
            self.proc_search_ebid_for_address(partner, ebid_settings, False)
            
        return True
    
    def proc_search_ebid_for_address(self, partner, ebid_settings, return_result=False):
        """
        Ermittlung der EBID-Nr für die Adressdaten des übergebenen Partnerdatensatzes
        :param partner: Adressdatensatz
        :param ebid_settings:
        :param return_result:
        :return: Vom Typ request_result_info, falls return_result True
        """
        eq_prot_obj = self[0].env['eq.ebid.protocol']
        eq_prot_position_obj = self[0].env['eq.ebid.protocol.position']
        
        success = False
        message = ""
        result_count = 0;
        prot_id = 0
        
        vals = {
                'companyName': partner.name,
                'street': partner.street,
                'zip': partner.zip,
                'city': partner.city,
                }
        
        if (partner.street2):
            vals['houseno'] = partner.street2

        searchRes = eq_ebid_services.find_company(partner.id, vals, ebid_settings)
        if (not searchRes):
            message = _('EBID could not be found for this address')
            
        else:
            if ((searchRes.searchHits) and (len(searchRes.searchHits) > 1)):
                sorted(searchRes.searchHits, key=lambda hit: hit.rate, reverse=True)
                
            protocol_for_partner = eq_prot_obj.sudo().search([('eq_res_id','=',partner.id), ('eq_model', '=', 'res.partner')])
            if (not protocol_for_partner):
                prot_id = eq_prot_obj.eq_create_protocol_entry(searchRes)
                
                if ((searchRes.searchHits) and (len(searchRes.searchHits) > 0)):
                    for search_res in searchRes.searchHits:
                        eq_prot_position_obj.create_position_for_company_search(prot_id, search_res)
                
            else:
                prot_id = protocol_for_partner.ids[0]
                protocol_record = eq_prot_obj.sudo().browse(prot_id)
                
                if (protocol_record):
                    protocol_record[0].eq_update_protocol_entry(searchRes)
                
                if (not searchRes.requestOK):
                    message = _('Search of EBID for address was not successful') 
                    if (searchRes.error):
                        message += '\n\n' + _('Error: ') + searchRes.error
                else:
                    if ((searchRes.searchHits) and (len(searchRes.searchHits) > 0)):
                        for search_res in searchRes.searchHits:
                            protocol_pos_for_partner = eq_prot_position_obj.sudo().search([('eq_ebid_protocol_id','=',prot_id), ('ebid_no', '=', search_res.ebid_no)])
                            
                            if (not protocol_pos_for_partner):
                                eq_prot_position_obj.create_position_for_company_search(prot_id, search_res)
                            else:
                                found_prot_pos = eq_prot_position_obj.sudo().browse(protocol_pos_for_partner.ids[0])
                                found_prot_pos.update_position_for_company_search(search_res)

            if (searchRes.requestOK and searchRes.searchHits):
                result_count = len(searchRes.searchHits)
                if (result_count != 1):
                    if (result_count == 0):
                        message = _('No EBID-Number could be found for this address')
                    elif (result_count > 1):
                        message = _('More than one EBID-Number were found for this address. Check the EBID protocol.')    
                else:
                    if (searchRes.searchHits[0].rate > ebid_settings.acceptance_rate):
                        found_ebid_no = searchRes.searchHits[0].ebid_no
                        if (found_ebid_no):
                            success = True
                            update_vals = {
                                           'eq_ebid_was_checked' : True,
                                           'eq_ebid_no' : found_ebid_no
                                           }
                            partner.write(update_vals)
            else:
                if (not searchRes.requestOK):
                    message = _('Search of EBID for address was not successful') 
                    if (searchRes.error):
                        message += '\n\n' + _('Error: ') + searchRes.error
                else:
                    message = _('No EBID-Number could be found for this address')

        if (return_result):
            return eq_ebid_services.request_result_info(success, result_count, message, prot_id)
        
    def show_message(self, info, message_text, prot_id):
        """
        Anzeige einer Meldung in Odoo
        :param info:
        :param message_text:
        :param prot_id:
        :return:
        """
        mod_obj = self.env['ir.model.data']
        view = mod_obj.get_object_reference('eq_partner_ebid_number', 'eq_message')
        
        vals = {
                'eq_info': info,
                'eq_message_text': message_text,       
                'eq_res_id' : prot_id, 
            }

        # set all data for or modal popup
        id = self.env['eq_message'].create(vals)
      
        return {
            'name': info,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [view and view[1] or False],
            'res_model': 'eq_message',
            'context': "{}",
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'res_id': id.id or False,                    
        }