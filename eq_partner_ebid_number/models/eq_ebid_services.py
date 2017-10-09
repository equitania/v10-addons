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

import requests
import json
from openerp import models, fields, api, _
from _ast import TryExcept


import logging
_logger = logging.getLogger(__name__)
    

"""
Funktionen für die Webservicerequests zum Unternehmensverzeichnis
"""


def settings_ok(settings):
    return settings and settings.user and settings.pw and settings.urlMatch


def get_ebid_settings(odoo_self):
    """

    :param odoo_self:
    :return:
    """
    config_params = odoo_self.env['ir.config_parameter']
    match_url = config_params.get_param("eq.ebid.service.match.url", False)
    company_url = config_params.get_param("eq.ebid.service.company.url", False)
    search_url = config_params.get_param("eq.ebid.service.search.url", False)
    homepage_url = config_params.get_param("eq.ebid.homepage.url", False) or 'http://www.unternehmensverzeichnis.org/'

    # logging
    logging_active_conf_val = config_params.get_param("eq.ebid.activate.log", False)
    if logging_active_conf_val:
        logging_active = True if (logging_active_conf_val == 'True' or logging_active_conf_val == 'true') else False
    else:
        logging_active = False
    # print 'homepage_url: ' + str(homepage_url)
    
    if (company_url and not company_url.endswith('/')):
        company_url += '/'
    if (homepage_url and not homepage_url.endswith('/')):
        homepage_url += '/'
    if (search_url and not search_url.endswith('/')):
        search_url += '/'
        
    user = config_params.get_param("eq.ebid.user", False)
    pw = config_params.get_param("eq.ebid.pw", False)
    rate_txt = config_params.get_param("eq.ebid.acceptance.rate", False)

    rate = 90
    if (rate_txt):
        rate = int(rate_txt)
    settings = EbidSettings(user, pw, match_url, company_url, search_url, homepage_url, logging_active, rate)
    return settings


def set_partner_identifier(ebid_settings):
    """
    TODO Noch umzusetzen
    :param ebid_settings:
    :return:
    """
    header = {'content-type': 'application/json'}
    contract_type = 'OdooAdminNutzer'
    eq_partner_key = 'TODO'

    url = "http://api.unternehmensverzeichnis.org/ws/crm/externalUserAdministration/rest/v2.0/externalLicenseContract/?externalLicenseKey=" + eq_partner_key + "&contractType=" + contract_type

    try:
        requestRes = requests.post(url, headers=header, auth=(ebid_settings.user, ebid_settings.pw))
        jsonRes = requestRes.json()

        if 'ErrorMessage' in jsonRes and jsonRes['ErrorMessage'] and ebid_settings.logging_active:
            write_to_log(ebid_settings.logging_active, 'Error in eq_ebid_services.set_partner_identifier:' + jsonRes['ErrorMessage'])
    except Exception, e:
        if ebid_settings.logging_active:
            write_to_log(ebid_settings.logging_active, 'Error in eq_ebid_services.set_partner_identifier: %s', True, e)


def write_to_log(do_log, message, is_error=False, exc=None):
    if not do_log:
        return

    if is_error:
        _logger.error(message, exc)
    else:
        _logger.info(message)


def find_company(partner_id, searchParams, ebid_settings):
    """
    Ermittlung der EBID über eine Suche anhand der Adressdaten
    :param partner_id:
    :param searchParams:
    :param ebid_settings:
    :return: EBIDRequestSearchResult: Ergebnis der Suche
    """
    header = {'content-type': 'application/json'}
    requestTxt = json.dumps(searchParams)
    try:
        requestRes = requests.post(ebid_settings.urlMatch, data=requestTxt, headers=header, auth=(ebid_settings.user, ebid_settings.pw))
        jsonRes = requestRes.json()
    except Exception, e:
        findCompanyResult = GetEBIDRequestResult(partner_id, "res.partner", None, None, False, 'Error [request findCompany]: ' + str(e.message), 1, requestTxt, requestRes.text)

        if ebid_settings.logging_active:
            write_to_log(ebid_settings.logging_active, 'Error in eq_ebid_services.find_company: %s', True, e)

        return findCompanyResult
    
    success = False
    foundID = ""
    error = ""
    searchResults = []  # EBIDRequestSearchResult

    respAsText = ''
    if requestRes.status_code == 200:
        success = True
        
        if (jsonRes) and (len(jsonRes) > 0):
            for res in jsonRes:
                foundID = res['ebid']
                rate = res['rate']
                
                rate_arr_txt = ''
                if 'rateArr' in res and res['rateArr']:
                    rate_arr = res['rateArr']
                    if (len(rate_arr) == 14):
                        rate_arr_txt = '{Street: ' + str(rate_arr[7]) + ', ' + 'HouseNo: ' + str(rate_arr[8]) + ', ' + 'City: ' + str(rate_arr[9]) + ', ' + 'Zip: ' + str(rate_arr[10]) + ', ' + 'CompanyName: ' + str(rate_arr[12]) + '}'
                    else:
                        rate_arr_conv = (str(sub_rate) for sub_rate in rate_arr)
                        rate_arr_txt = '{' + ','.join(rate_arr_conv) + '}'
                    
                respAsText += '[EBID: ' + str(foundID) + ', Rate: ' + str(rate) + ', Rate_Arr: ' + rate_arr_txt + ']; '
                
                searchResultItem = EBIDRequestSearchResult(success, "", foundID, rate, rate_arr_txt, rate > ebid_settings.acceptance_rate)
                searchResults.append(searchResultItem)
        else:
            error = "No result found"
    else:
        respAsText = requestRes.text

        if 'ErrorMessage' in jsonRes and jsonRes['ErrorMessage'] and ebid_settings.logging_active:
            write_to_log(ebid_settings.logging_active, 'Error in eq_ebid_services.find_company:' + jsonRes['ErrorMessage'])

        if (len(jsonRes) > 0) and 'ErrorMessage' in jsonRes:
            error = jsonRes['ErrorMessage']
        else:
            error = "Error"
    findCompanyResult = GetEBIDRequestResult(partner_id, "res.partner", searchResults, None, success, error, 1, requestTxt, respAsText)  # requestRes.text)
    
    return findCompanyResult


def get_search_as_you_type_token(ebid_settings):
    header = {'content-type': 'application/json'}
    try:
        requestRes = requests.get(ebid_settings.urlCompany + ebid, headers=header,
                                  auth=(ebid_settings.user, ebid_settings.pw))
        jsonRes = requestRes.json()
    except Exception, e:
        findCompanyResult = GetEBIDRequestResult(partner_id, "res.partner", None, None, False,
                                                 'Error [request get_company_for_ebid]: ' + e.message, 1,
                                                 'ebid: ' + ebid, requestRes.text)
        return findCompanyResult


def get_company_for_ebid(partner_id, ebid, ebid_settings):
    """
    Aufruf des Companyservices für Suche einer Firma über die EBID-Nr
    :param partner_id: 
    :param ebid: 
    :param ebid_settings: 
    :return: 
    """
    header = {'content-type': 'application/json'}  
    try:
        requestRes = requests.get(ebid_settings.urlCompany + ebid, headers=header, auth=(ebid_settings.user, ebid_settings.pw))
        jsonRes = requestRes.json()
    except Exception, e:
        if ebid_settings.logging_active:
            write_to_log(ebid_settings.logging_active, 'Error in eq_ebid_services.get_company_for_ebid: %s', True, e)

        findCompanyResult = GetEBIDRequestResult(partner_id, "res.partner", None, None, False, 'Error [request get_company_for_ebid]: ' + e.message, 1, 'ebid: ' + ebid, requestRes.text)
        return findCompanyResult
     
    error = ''
    respAsText = ''
    success = False
    search_res = False
    if requestRes.status_code == 200:
        success = True
        if (jsonRes) and (len(jsonRes) > 0):
            search_res = SearchForEBIDResult(ebid, jsonRes)
            
    else:
        if 'ErrorMessage' in jsonRes and jsonRes['ErrorMessage'] and ebid_settings.logging_active:
            write_to_log(ebid_settings.logging_active, 'Error in eq_ebid_services.get_company_for_ebid:' + jsonRes['ErrorMessage'])

        respAsText = requestRes.text
        if (len(jsonRes) > 0) and 'ErrorMessage' in jsonRes:
            error = jsonRes['ErrorMessage']
    
    search_ebid_result = GetEBIDRequestResult(partner_id, "res.partner", None, search_res, success, error, 2, '', respAsText);
    
    return search_ebid_result


class request_result_info:
    def __init__(self, success, result_count, message, res_id=0):
        self.success = success
        self.result_count = result_count
        self.message = message
        self.res_id = res_id


class EbidSettings:
    """
    Kapselung der Konfigurationsdaten
    """

    def __init__(self, user, pw, matchUrl, companyUrl, searchUrl, homepage, logging_active=False, acceptance_rate=90):
        self.user = user
        self.pw = pw 
        self.urlMatch = matchUrl
        self.urlCompany = companyUrl
        self.urlSearch = searchUrl
        self.homepage = homepage
        self.logging_active = logging_active
        self.acceptance_rate = acceptance_rate


class GetEBIDRequestResult:
    def __init__(self, res_id, model, resultList, ebid_search_result, success, errorMsg, request_type, request="", response=""):
        self.res_id = res_id
        self.searchHits = resultList
        self.requestOK = success
        self.error = errorMsg
        self.request = request
        self.response = response
        self.model = model
        self.request_type = request_type
        self.ebid_search_result = ebid_search_result
        

class EBIDRequestSearchResult:
    
    def __init__(self, success, errorMsg, ebidno, rate=0, arr_rate='', above_rate=False):
        self.requestOK = success
        self.error = errorMsg
        self.ebid_no = ebidno
        self.rate = rate
        self.arr_rate = arr_rate


class SearchForEBIDResult:
    """
    Hilfsklasse für Speicherung des Ergebnisses einer Suche über die EBID
    """

    def __init__(self, ebidno, values):
        """
        Auslesen der Firmendaten aus Ergebnis des Company-Services
        :param ebidno: 
        :param values: 
        """
        self.ebid_no = ebidno

        self.phone = ''
        self.fax = ''
        self.mobile = ''
        self.email = ''
        self.url = ''
        self.company_name = ''
        self.street = ''
        self.house_no = ''
        self.city = ''
        self.city_part = ''
        self.zip = ''
        self.country = ''

        if (values):
            company_name_res = values['companyName']
            address_dict = {}
            if isinstance(company_name_res, dict) and 'address' in values:
                # neue API
                address_dict = values.get('address', {})
                self.company_name = company_name_res['value']
                self.ustid_nr = values.get('vatNo', '')

                if 'phoneNumbers' in values:
                    phoneNumbers = values['phoneNumbers']
                    for phoneNo in phoneNumbers:
                        if 'number' in phoneNo and 'type' in phoneNo:
                            type = phoneNo['type']
                            if 'priority' in phoneNo and phoneNo['priority'] != 'Primary':
                                continue
                            if type == 'Phone':
                                self.phone = phoneNo['number']
                            if type == 'Fax':
                                self.fax = phoneNo['number']
                            if type == 'Mobile':  # ?
                                self.mobile = phoneNo['number']

                if 'emails' in values:
                    emails = values['emails']
                    for email in emails:
                        if 'email' in email:
                            if 'priority' in email and email['priority'] != 'Primary':
                                continue
                            self.email = email['email']

                if 'urls' in values:
                    urls = values['urls']
                    for url in urls:
                        if 'url' in url:
                            if 'priority' in url and url['priority'] != 'Primary':
                                continue
                            self.url = url['url']

            else:
                # alte API
                address_dict = values
                self.company_name = address_dict['companyName']
                self.ustid_nr = address_dict['ustIdNr']

                self.phone = address_dict['phone']
                self.fax = address_dict['fax']
                self.mobile = address_dict['mobile']
                self.email = address_dict['email']
                self.url = address_dict['url']

            self.street = address_dict['street']
            self.house_no = address_dict['houseNo']
            self.city = address_dict['city']
            self.city_part = address_dict['cityPart']
            self.zip = address_dict['zip']
            self.country = address_dict['country']
