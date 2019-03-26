# -*- coding: utf-8 -*-
# Copyright Equitania Software GmbH - Germany - https://www.equitania.de
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class EqInstallDefaultReportsFunc(models.Model):
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
            attachment = print_report_name \
                = "(object.state in ('open','paid')) " \
                  "and ('Rechnung-'+(object.number or '').replace('/','')+'.pdf') " \
                  "or (object.state in ('draft')) " \
                  "and ('Rechnungsentwurf'+(object.number or '').replace('/','')+'.pdf')"
        elif report_name == "Request for Quotation":        # Angebotsanfrage
            attachment = print_report_name \
                = "('Einkaufsanfrage-' + (object.name or '').replace('/','')+'.pdf')"
        elif report_name == "Purchase Order":               # Beschaffungsauftrag
            attachment = print_report_name \
                = "('Einkauf-' + (object.name or '').replace('/','')+'.pdf')"
        elif report_name == "Quotation / Order":            # Angebot
            attachment = print_report_name \
                = "(object.state in ('draft','sent')) " \
                  "and ('Angebot-' + (object.name or '').replace('/','')+'.pdf') " \
                  "or (object.state in ('sale','done')) " \
                  "and ('Auftrag-' + (object.name or '').replace('/','')+'.pdf')"
        elif report_name == "Delivery Slip":                # Lieferschein (Lager)
            attachment = print_report_name \
                = "('Lieferschein-' + (object.name or '').replace('/','')+'.pdf')"
        elif report_name == "Picking Operations":           # Packvorgänge (Lager)
            attachment = print_report_name\
                = "('Packschein-' + (object.name or '').replace('/','')+'.pdf')"

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
