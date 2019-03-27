# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, _


#Adds a Search for the Positions of a pricelist.

#
# class eq_pricelist_item_search(models.Model):
#     _name = "eq_pricelist_item_search"
#
#     eq_items_id = fields.Many2one('product.pricelist.item', 'Item')
#
#
#     def open(self, context):
#         """
#         Aufgerufen aus Dialog für Positionssuche
#         Öffnet die Detailansicht einer Preislistenposition
#         :param context:
#         :return:
#         """
#         mod_obj = self.env['ir.model.data']
#         # item = self.pool.get('eq_pricelist_item_search').browse(cr, uid, ids, context)
#         self._cr.execute("DELETE FROM eq_pricelist_item_search",)
#         res = mod_obj.get_object_reference('eq_pricelist', 'eq_pricelist_item_search_item_form')
#
#         res_id = False
#         if 'params' in context and 'item' in context['params']:
#             res_id = context['params']['item']
#
#         return {
#             'name': 'Item',
#             'view_type': 'form',
#             'view_mode': 'form',
#             'view_id': [res and res[1] or False],
#             'res_model': 'product.pricelist.item',
#             'context': "{}",
#             'type': 'ir.actions.act_window',
#             'nodestroy': True,
#             'target': 'new',
#             'res_id': res_id or False,
#         }


class EqProductPricelistItem(models.Model):
    """EqProductPricelistItem class inherited from ProductPricelistItem class"""
    _inherit = 'product.pricelist.item'

    _columns = {}

    @api.one
    def delete(self):
        self.unlink()
        return True

    @api.multi
    def name_get(self):
        # if self._context is None:
        #     self._context = {}

        res = []
        for record in self:
            name = _("%s, Min. %s New Price %s") % (record.name, record.min_quantity, record.price_surcharge)
            res.append((record.id, name))
        return res
