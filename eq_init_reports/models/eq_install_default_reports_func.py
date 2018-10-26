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


class eq_install_default_reports_func(models.Model):
    """
    Our small helper that will set defined reports to FastReports reports with all default data
    """
    _name = "eq_install_default_reports_func"

    eq_report_names = [
        "Invoices",
        "Request for Quotation",
        "Purchase Order",
        "Quotation / Order",
        "Delivery Slip",
        "Picking Operations"
    ]

    def set_report_settings(self, report_name):
        """
        Sett extra report settings like attachment and print report name
        :param report_name: Actual report
        :return: Generated attachment and print report name for actual report
        """
        attachment = print_report_name = ""
        if report_name == "Invoices":                       # Rechnung
            attachment = print_report_name = "(object.state in ('open','paid')) and ('Rechnung-'+(object.number or '').replace('/','')+'.pdf')"
        elif report_name == "Request for Quotation":        # Angebotsanfrage
            attachment = print_report_name = "('Einkaufanfrage-' + (object.name or '').replace('/','')+'.pdf')"
        elif report_name == "Purchase Order":               # Beschaffungsauftrag
            attachment = print_report_name =  "('Einkauf-' + (object.name or '').replace('/','')+'.pdf')"
        elif report_name == "Quotation / Order":            # Angebot
            attachment = print_report_name = "(object.state in ('draft','sent')) and ('Angebot-' + (object.name or '').replace('/','')+'.pdf') or (object.state in ('sale','done')) and ('Auftrag-' + (object.name or '').replace('/','')+'.pdf')"
        elif report_name == "Delivery Slip":                # Lieferschein (Lager)
            attachment = print_report_name = "('Lieferschein-' + (object.name or '').replace('/','')+'.pdf')"
        elif report_name == "Picking Operations":           # Packvorgänge (Lager)
            attachment = print_report_name = "('Packschein-' + (object.name or '').replace('/','')+'.pdf')"

        return attachment, print_report_name

    def _set_default_reports(self):
        """
        Set report and all parametes
        """
        ir_act_report_xml_obj = self.env['ir.actions.report.xml']
        for report_name in self.eq_report_names:
            report = ir_act_report_xml_obj.search([("name", "=", report_name)], limit=1)
            if report:
                report.attachment, report.print_report_name = self.set_report_settings(report_name)

                # update report data
                ir_act_report_xml_obj.write(report)
