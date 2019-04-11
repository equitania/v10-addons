# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import http, tools, _
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request
import odoo


class EqWebSiteSaleController(WebsiteSale):

    @http.route('/get_server_infos_json', type='json', auth='public')
    def get_server_infos_json(self):
        """
        Helper method called from frontend after click on "?" link
        We're getting systeminfos here and use it during call of help
        :return: JSON Object with system infos
        """
        result = {}
        conf_param_obj = request.env['ir.config_parameter']
        res1 = conf_param_obj.search([('key', '=', 'help_server_path')])
        result["help_server_path"] = res1.value

        res2 = conf_param_obj.search([('key', '=', 'web.base.url')])
        result["base_url"] = res2.value

        version_info = odoo.service.common.exp_version()
        result["software_version"] = str(version_info["server_version_info"][0])
        return result
