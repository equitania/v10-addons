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

class eq_product_product(models.Model):
    _inherit = 'product.product'

    eq_drawing_number = fields.Char('Drawing Number', size=50)


class eq_product_template(models.Model):
    _inherit = 'product.template'

    eq_drawing_number = fields.Char('Drawing Number', size=50)

    #
    # """
    # _defaults = {
    #              'eq_sale_min_qty': 0,
    # }
    # """
    #
    # def action_view_stock_moves(self, cr, uid, ids, context=None):
    #     products = self._get_products(cr, uid, ids, context=context)
    #     result = self._get_act_window_dict(cr, uid, 'stock.act_product_stock_move_open', context=context)
    #     if len(ids) == 1 and len(products) == 1:
    #         ctx = "{'tree_view_ref':'stock.view_move_tree', \
    #               'default_product_id': %s, 'search_default_product_id': %s}" \
    #               % (products[0], products[0])
    #         result['context'] = ctx
    #     else:
    #         result['domain'] = "[('product_id','in',[" + ','.join(map(str, products)) + "])]"
    #         result['context'] = "{'tree_view_ref':'stock.view_move_tree'}"
    #     return result
    #
    # def action_view_stock_moves(self, cr, uid, ids, context=None):
    #     products = self._get_products(cr, uid, ids, context=context)
    #     result = self._get_act_window_dict(cr, uid, 'equitania.eq_act_product_stock_move_open', context=context)
    #     if len(ids) == 1 and len(products) == 1:
    #         ctx = "{'tree_view_ref':'stock.view_move_tree', \
    #               'default_product_id': %s, 'search_default_product_id': %s}" \
    #               % (products[0], products[0])
    #         result['context'] = ctx
    #         result['context'] = result['context'][:-1] + ", 'search_default_in_and_out': 1" + result['context'][-1]
    #     else:
    #         result['domain'] = "[('product_id','in',[" + ','.join(map(str, products)) + "])]"
    #         result['context'] = result['context'][:-1] + ", 'search_default_in_and_out': 1" + result['context'][-1]
    #     return result

    @api.multi
    def write(self, vals):
        """
        Überschreiben der write-Methode für Preishistorie und Setzen der Übersetzung für Feld name
        :param ids:
        :param vals:
        :return:
        """
        if 'standard_price' in vals:
            old_price = self.standard_price
            new_price = vals['standard_price']
            history_vals = {
                'eq_product_id': self.id,
                'eq_old_price': old_price,
                'eq_new_price': new_price,
            }
            self.env['product.template.standard_price_history'].create(history_vals)
        res = super(eq_product_template, self).write(vals)

        # Korrektur der Lokalisierung für das Feld name, damit wir kein Problem mehr mit dem Modul web_translate haben
        if self._context is not None:
            if 'lang' in self._context and 'name' in vals:  # sehr wichtig ! die Write-Methode wird ausgeführt auch wenn man in den Einstellungen etwas speichert !
                actual_language = self._context['lang']
                text_to_be_set = vals['name']
                ir_translation_obj = self.env['ir.translation']
                ir_translation_record = ir_translation_obj.sudo().search([('res_id', '=', self.id), (
                'lang', '=', actual_language), ('name', '=', 'product.template,name')])
                if ir_translation_record:
                    ir_translation_record.value = text_to_be_set

        return res


class eq_product_template_standard_price_history(models.Model):
    _name = 'product.template.standard_price_history'
    # _rec_name = 'create_date'

    eq_product_id = fields.Many2one('product.template', string="Product")
    eq_old_price = fields.Float(string="Old Price", digits=dp.get_precision('Product Price Purchase'))
    eq_new_price = fields.Float(string="New Price", digits=dp.get_precision('Product Price Purchase'))
    create_uid = fields.Many2one('res.users', string="User")
    create_date = fields.Datetime(string="Create Date")

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, _('Change ') + self.create_date))

        return res

