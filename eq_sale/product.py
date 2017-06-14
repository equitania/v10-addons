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
import odoo.addons.decimal_precision as dp


class eq_product_template(models.Model):
    _inherit = 'product.template'

    @api.one
    def _eq_sale_count(self):
        """
        Überschreiben der bisherigen Anzahl für die Verkäufe für den Smartbutton in der Produktansicht
        Änderungen für Status in Odoo10:
        - done: Odoo8 = erledigt, Odoo10: done=Gesperrt, sale=Verkaufsauftrag
        :return:
        """
        res = ''

        query = """select sum(product_uom_qty) from stock_move where procurement_id in
        (select id from procurement_order where sale_line_id in
        (select id from sale_order_line as sol where sol.product_id in
        (select id from product_product where product_tmpl_id = %d)
        and sol.state not in ('cancel')
        and (select state from sale_order where id = sol.order_id) not in ('sent', 'draft')))
        and state not in ('sale', 'done', 'cancel')
        and picking_id is not null""" % (self.id)
        self._cr.execute(query)
        open = self._cr.fetchone()[0] or 0
        qry_all = """select sum(product_uom_qty) from sale_order_line where product_id in (select id from product_product where product_tmpl_id = %d) and state != 'cancel' and state != 'done' and (select state from sale_order where id = order_id) not in ('sent', 'draft')""" % (
                self.id)
        self._cr.execute(qry_all)
        all = self._cr.fetchone()[0] or 0
        res = '%d / %d' % (open, all)
        self.eq_sale_count = res

    eq_sale_count = fields.Char(compute='_eq_sale_count', string="Sales")


class eq_product_product(models.Model):
    _inherit = 'product.product'

    @api.one
    def _eq_sale_count(self):
        """
        Überschreiben der bisherigen Anzahl der Verkäufe für den Smartbutton in der Produktansicht
        neu: Anzeige offen/gesamt
        :return:
        """

        qry_open = """select sum(product_uom_qty) from stock_move where procurement_id in 
        (select id from procurement_order where sale_line_id in 
        (select id from sale_order_line as sol where sol.product_id  = %d 
        and sol.state not in ('cancel', 'done') 
        and (select state from sale_order where id = sol.order_id) not in ('sent', 'draft'))) 
        and state not in ('done', 'cancel', 'sale')
        and picking_id is not null""" % (self.id)

        self._cr.execute(qry_open)
        open = self._cr.fetchone()[0] or 0

        qry_all = """select sum(product_uom_qty) from sale_order_line where product_id = %d and state != 'cancel'  and state != 'done' 
        and (select state from sale_order where id = order_id) not in ('sent', 'draft')""" % (self.id)

        self._cr.execute(qry_all)
        all = self._cr.fetchone()[0] or 0
        res = '%d / %d' % (open, all)
        self.eq_sale_count = res


    eq_sale_count = fields.Char(compute='_eq_sale_count', string="Sales")