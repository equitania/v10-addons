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


class report_stock_picking(models.Model):
    _inherit = 'stock.picking'

    # def get_tax(self, tax_id, language, currency_id):
    #     amount_net = 0;
    #     for line in self.order_line:
    #         if tax_id.id in [x.id for x in line.tax_id] and not line.eq_optional:
    #             amount_net += line.price_subtotal
    #
    #     tax_amount = 0
    #     for tex in self.env['account.tax']._compute([tax_id], amount_net, 1):
    #         tax_amount += tex['amount']
    #
    #     return self.env["eq_report_helper"].get_price(tax_amount, language, 'Sale Price Report', currency_id)
    #
    #
    # @api.multi
    # def get_price(self, value, currency_id, language):
    #     """
    #     Formatierung eines Preises mit Berücksichtigung der Einstellung Dezimalstellen Sale Price Report
    #     :param value:
    #     :param currency_id:
    #     :param language:
    #     :return:
    #     """
    #     return self.env["eq_report_helper"].get_price(value, language, 'Sale Price Report', currency_id)
    #
    # @api.multi
    # def get_qty(self, value, language):
    #     """
    #     Formatierung für Mengenangabe mit Berücksichtigung der Einstellung Dezimalstellen Sale Quantity Report
    #     :param value:
    #     :param language:
    #     :return:
    #     """
    #     return self.env["eq_report_helper"].get_qty(value, language, 'Sale Quantity Report')

    @api.multi
    def html_text_is_set(self, value):
        """
        Workaround für HTML-Texte: Autom. Inhalt nach Speichern ohne Inhalt: <p><br></p>
        Entfernen der Zeilenumbrüche und Paragraphen für Test, ob ein Inhalt gesetzt wurde
        :param value:
        :return:
        """
        if not value:
            return False

        value = value.replace('<br>', '')
        value = value.replace('<p>', '')
        value = value.replace('</p>', '')
        value = value.replace('<', '')
        value = value.replace('>', '')
        value = value.replace('/', '')
        value = value.strip()
        return value != ''