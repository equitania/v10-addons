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

from odoo import fields, models

class eq_product_template_fa(models.Model):
    _inherit = 'product.template'
    
    def _eq_fa_count_sale(self, ids):
        res = {}
        for id in ids:
            self.env.cr.execute("""select count(*) FROM (select eq_agreement_id from eq_framework_agreement_pos as pos where eq_product_id in (select id from product_product where product_tmpl_id = %d) and eq_quantity > coalesce((select sum(eq_quantity) from eq_framework_agreement_pos_fetches where eq_pos_id = pos.id), 0) group by eq_agreement_id) as test""" % (id))
            open = self.env.cr.fetchone() or [0]
            self.env.cr.execute("""select count(*) FROM (select eq_agreement_id from eq_framework_agreement_pos as pos where eq_product_id in (select id from product_product where product_tmpl_id = %d) group by eq_agreement_id) as test""" % (id))
            all = self.env.cr.fetchone() or [0]
            res[id] = '%d / %d' % (open[0], all[0])
        return res
    

    #eq_fa_count_sale = fields.Function(_eq_fa_count_sale, type="char")

    
    def action_view_fas_sale(self, ids, context=None):
        act_obj = self.env['ir.actions.act_window']
        mod_obj = self.env['ir.model.data']
        product_ids = []
        for template in self.browse(ids, context=context):
            product_ids += [x.id for x in template.product_variant_ids]
        result = mod_obj.xmlid_to_res_id('eq_framework_agreement.action_eq_framework_agreement_tree',raise_if_not_found=True)
        result = act_obj.read([result], context=context)[0]
        result['domain'] = "[('eq_product_id','in',[" + ','.join(map(str, product_ids)) + "])]"
        return result
    
class eq_product_product_fa(models.Model):
    _inherit = 'product.product'
    
    def _eq_fa_count_sale(self, ids):
        res = {}
        for id in ids:
            self.env.cr.execute("""select count(*) FROM (select eq_agreement_id from eq_framework_agreement_pos as pos where eq_product_id = %d and eq_quantity > coalesce((select sum(eq_quantity) from eq_framework_agreement_pos_fetches where eq_pos_id = pos.id), 0) group by eq_agreement_id) as test""" % (id))
            open = self.env.cr.fetchone() or [0]
            self.env.cr.execute("""select count(*) FROM (select eq_agreement_id from eq_framework_agreement_pos as pos where eq_product_id = %d group by eq_agreement_id) as test""" % (id))
            all = self.env.cr.fetchone() or [0]
            res[id] = '%d / %d' % (open[0], all[0])
        return res
    

    eq_fa_count_sale = fields.Char(compute=_eq_fa_count_sale, type="char")
