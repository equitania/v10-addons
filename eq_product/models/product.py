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
from string import replace


class eq_product_product(models.Model):
    _inherit = 'product.product'

    # Nachfolgende Constraintdefinition erfolgt nur, wenn es bisher keine Produkte gibt, welche gegen diese Constraint verstoßen.
    # https://www.odoo.com/forum/help-1/question/why-sql-constraints-not-working-39549

    _sql_constraints = [
        ('default_code_unique', 'unique(default_code)', "This Product No. is already in use!"),
    ]


    def _generate_ean(self, company_ean, sequence):
        ean_without_checksum = company_ean + sequence[-5:]

        oddsum = 0
        evensum = 0
        for i in range(0, len(ean_without_checksum)):
            if i % 2 == 0:
                oddsum += int(ean_without_checksum[i])
            else:
                evensum += int(ean_without_checksum[i])
        total = oddsum + (evensum * 3)
        checksum = int(10 - total % 10.0) % 10
        if checksum == 10:
            checksum == 0
        ean13 = ean_without_checksum + str(checksum)
        self.write({'ean13': ean13})

    @api.model
    def create(self, vals):
        """
        Unsere Erweiterung der CREATE Methode
        :param vals:
        :return:
        """
        res = super(eq_product_product, self).create(vals)

        # Nummer wurde nicht eingegeben, wir müssen sie generieren
        if 'default_code' not in vals or vals['default_code'] is False:
            self.eq_product_number_update(res)
            res.barcode = res.default_code

        return res

    @api.multi
    def eq_product_number_update(self, res):
        if self.id is False:
            self = res

        product_product_obj = self.env['product.product'].browse(self.id)

        seq = self.env['ir.sequence'].get('eq_product_no')
        vals = {
            'default_code': seq
        }

        product_product_obj.write(vals)

    # @api.multi
    # def eq_product_number_update(self, context):
    #     # Gets the product
    #     for product in self:
    #         # product = self # self.env['product.product'].browse(ids)
    #         prod_rec = product.default_code
    #
    #         # Gets the config values for the product number
    #         ir_values = self.env['ir.values']
    #         min_prefix_count = ir_values.get_default('product.product', 'default_eq_min_prefix_count')
    #         max_prefix_count = ir_values.get_default('product.product', 'default_eq_max_prefix_count')
    #         prod_num_lenght = ir_values.get_default('product.product', 'default_eq_prod_num_lenght')
    #         seperator = ir_values.get_default('product.product', 'default_eq_seperator')
    #         # Deletes all spaces in the string
    #         if prod_rec:
    #             prod_rec = replace(prod_rec, ' ', '')
    #             if seperator:
    #                 prod_rec = replace(prod_rec, seperator, '')
    #             else:
    #                 seperator = ''
    #                 prod_rec = replace(prod_rec, seperator, '')
    #         else:
    #             prod_rec = ''
    #             seperator = ''
    #         if len(prod_rec) >= min_prefix_count and len(prod_rec) <= max_prefix_count:
    #             # Sql Query (self explaining), which gets the entries where prefix is identical to prefix.
    #             self._cr.execute("Select * From ir_sequence Where code=%s", ('eq_product_no.' + prod_rec,))
    #
    #             # cr.fetchone is a dictionary with the row from the database. which we got with cr.execute
    #             # If the sequence with the prefix is present, we just use the sequence
    #             if self._cr.fetchone():
    #                 # Gets the sequence for the and sets it in the appropriate field
    #                 seq = self.env['ir.sequence'].get('eq_product_no.' + prod_rec)
    #                 vals = {
    #                     'default_code': seq
    #                 }
    #
    #                 # Test
    #                 product._generate_ean('1234567890123', seq)
    #
    #                 super(eq_product_product, product).write(vals)
    #                 if prod_rec == '' and max_prefix_count == 0:
    #                     company_ean = self.env['res.users'].browse(self._uid).company_id.eq_company_ean
    #                     if company_ean:
    #                         product._generate_ean(company_ean, seq)
    #
    #             # Else we create that sequence and the sequence.type and use it
    #             else:
    #                 # Defines the sequence.type
    #
    #                 # auskommentiert in Odoo10
    #                 # vals_seq_type = {
    #                 #     'code': 'eq_product_no.' + prod_rec,
    #                 #     'name': 'Product Number ' + prod_rec,
    #                 # }
    #
    #                 # Creates the sequence.type in OpenERP; auskommentiert in Odoo10
    #                 # self.env['ir.sequence.type'].create(vals_seq_type, context)
    #
    #                 # Gets the company_id, which is needed for the sequence
    #                 user_rec = self.env['res.users'].browse(self._uid)
    #                 company_id = user_rec.company_id.id
    #
    #                 # Defines the sequence and uses the ir.sequence.type that was previously created
    #                 vals_seq = {
    #                     'code': 'eq_product_no.' + prod_rec,
    #                     'suffix': '',
    #                     'number_next': 1,
    #                     'number_increment': 1,
    #                     'implementation': 'standard',
    #                     'company_id': company_id,
    #                     'padding': prod_num_lenght,
    #                     'active': True,
    #                     'prefix': prod_rec + seperator,
    #                     'name': 'Product Number ' + prod_rec,
    #                 }
    #                 # Creates the sequence in OpenERP
    #                 self.env['ir.sequence'].create(vals_seq)
    #
    #                 # Gets the sequence for the and sets it in the appropriate field
    #                 seq = self.env['ir.sequence'].get('eq_product_no.' + prod_rec)
    #
    #                 # Test
    #                 product._generate_ean('1234567890123', seq)
    #
    #                 vals = {
    #                     'default_code': seq
    #                 }
    #                 super(eq_product_product, product).write(vals)
    #                 if prod_rec == '' and max_prefix_count == 0:
    #                     company_ean = self.env['res.users'].browse(self._uid).company_id.eq_company_ean
    #                     if company_ean:
    #                         product._generate_ean(company_ean, seq)


class eq_product_template(models.Model):
    _inherit = 'product.template'


    #Nachfolgende Constraintdefinition erfolgt nur, wenn es bisher keine Produkte gibt, welche gegen diese Constraint verstoßen.
    #https://www.odoo.com/forum/help-1/question/why-sql-constraints-not-working-39549

    _sql_constraints = [
        ('default_code_unique', 'unique(default_code)', "This Product No. is already in use!"),
    ]


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

    # @api.model
    # def create(self, vals):
    #     """
    #     Unsere Erweiterung der CREATE Methode
    #     :param vals:
    #     :return:
    #     """
    #     res = super(eq_product_template, self).create(vals)
    #
    #     # Nummer wurde nicht eingegeben, wir müssen sie generieren
    #     if 'default_code' not in vals or vals['default_code'] is False:
    #         self.eq_product_number_update(res)
    #         res.barcode = res.default_code
    #
    #     return res

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

    # @api.multi
    # def eq_product_number_update(self, res):
    #     if self.id is False:
    #         self = res
    #
    #     product_obj = self.env['product.template'].browse(self.id)
    #
    #     seq = self.env['ir.sequence'].get('eq_product_no')
    #     vals = {
    #         'default_code': seq
    #     }
    #
    #     product_obj.write(vals)


    # @api.multi
    # def eq_product_number_update(self, res):
    #     """
    #     Generierung der Produktnummer in product.template
    #     :param ids:
    #     :return:
    #     """
    #
    #     if self.id is False:
    #         self = res
    #
    #     product_obj = self.env['product.product']
    #     product = self.env['product.template'].browse(self.id)
    #     prod_rec = product[0].default_code
    #
    #     # Gets the config values for the product number
    #     ir_values = self.env['ir.values']
    #     min_prefix_count = ir_values.get_default('product.product', 'default_eq_min_prefix_count')
    #     max_prefix_count = ir_values.get_default('product.product', 'default_eq_max_prefix_count')
    #     prod_num_lenght = ir_values.get_default('product.product', 'default_eq_prod_num_lenght')
    #     seperator = ir_values.get_default('product.product', 'default_eq_seperator')
    #     # Deletes all spaces in the string
    #     if prod_rec:
    #         prod_rec = replace(prod_rec, ' ', '')
    #         if seperator:
    #             prod_rec = replace(prod_rec, seperator, '')
    #         else:
    #             seperator = ""
    #     else:
    #         prod_rec = ''
    #         seperator = ''
    #     if len(prod_rec) >= min_prefix_count and len(prod_rec) <= max_prefix_count:
    #         # Sql Query (self explaining), which gets the entries where prefix is identical to prefix.
    #         self._cr.execute("Select * From ir_sequence Where code=%s", ('eq_product_no.' + prod_rec,))
    #
    #         # If the sequence with the prefix is present, we just use the sequence
    #         if self._cr.fetchone():
    #             # Gets the sequence for the and sets it in the appropriate field
    #             seq = self.env['ir.sequence'].get('eq_product_no.' + prod_rec)
    #             vals = {
    #                 'default_code': seq
    #             }
    #
    #             if product[0].product_variant_ids:
    #                 product[0].product_variant_ids[0].write(vals)
    #                 if prod_rec == '' and max_prefix_count == 0:
    #                     try:
    #                         company_ean = self.env['res.users'].browse(uid).company_id.eq_company_ean
    #                         if company_ean:
    #                             product_obj._generate_ean(product[0].product_variant_ids[0], company_ean, seq)
    #                     except:
    #                         # vorläufig wegen fehlendem Feld eq_company_ean
    #                         pass
    #
    #         # Else we create that sequence and the sequence.type and use it
    #         else:
    #             # Defines the sequence.type
    #             vals_seq_type = {
    #                 'code': 'eq_product_no.' + prod_rec,
    #                 'name': 'Product Number ' + prod_rec,
    #             }
    #
    #             # Creates the sequence.type in OpenERP; auskommentiert in Odoo10
    #             # self.env['ir.sequence.type'].create(vals_seq_type)
    #
    #             # Gets the company_id, which is needed for the sequence
    #             user_rec = self.env['res.users'].browse(self._uid)
    #             company_id = user_rec.company_id.id
    #
    #             # Defines the sequence and uses the ir.sequence.type that was previously created
    #             vals_seq = {
    #                 'code': 'eq_product_no.' + prod_rec,
    #                 'suffix': '',
    #                 'number_next': 1,
    #                 'number_increment': 1,
    #                 'implementation': 'standard',
    #                 'company_id': company_id,
    #                 'padding': prod_num_lenght,
    #                 'active': True,
    #                 'prefix': prod_rec + seperator,
    #                 'name': 'Product Number ' + prod_rec,
    #             }
    #             # Creates the sequence in OpenERP
    #             self.env['ir.sequence'].create(vals_seq)
    #
    #             # Gets the sequence for the and sets it in the appropriate field
    #             seq = self.env['ir.sequence'].get('eq_product_no.' + prod_rec)
    #             vals = {
    #                 'default_code': seq
    #             }
    #
    #             if product[0].product_variant_ids:
    #                 product[0].product_variant_ids[0].write(vals)  # ?
    #
    #             # product_obj.write(product_variant, vals)
    #             if prod_rec == '' and max_prefix_count == 0:
    #                 try:
    #                     company_ean = self.env['res.users'].browse(uid, context).company_id.eq_company_ean
    #                     if company_ean:
    #                         product_obj._generate_ean(product[0].product_variant_ids[0], company_ean, seq)
    #                 except:
    #                     # try vorläufig wegen fehlendem Feld eq_company_ean
    #                     pass

        def _generate_ean(self, prod_variant, company_ean, sequence):
            ean_without_checksum = company_ean + sequence[-5:]

            oddsum = 0
            evensum = 0
            for i in range(0, len(ean_without_checksum)):
                if i % 2 == 0:
                    oddsum += int(ean_without_checksum[i])
                else:
                    evensum += int(ean_without_checksum[i])
            total = oddsum + (evensum * 3)
            checksum = int(10 - total % 10.0) % 10
            if checksum == 10:
                checksum == 0
            ean13 = ean_without_checksum + str(checksum)
            prod_variant.write({'ean13': ean13})


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


class eq_sale_config_product(models.TransientModel):
    _inherit = 'sale.config.settings'

    def set_default_prod_config_values(self):
        ir_values_obj = self.env['ir.values']

        ir_values_obj.set_default('product.product', 'default_eq_min_prefix_count', self.default_eq_min_prefix_count)
        ir_values_obj.set_default('product.product', 'default_eq_max_prefix_count', self.default_eq_max_prefix_count)
        ir_values_obj.set_default('product.product', 'default_eq_prod_num_lenght', self.default_eq_prod_num_lenght)
        ir_values_obj.set_default('product.product', 'default_eq_seperator', self.default_eq_seperator)

    def get_default_prod_config_values(self, fields):
        ir_values_obj = self.env['ir.values']

        default_eq_min_prefix_count = ir_values_obj.get_default('product.product', 'default_eq_min_prefix_count')
        default_eq_max_prefix_count = ir_values_obj.get_default('product.product', 'default_eq_max_prefix_count')
        default_eq_prod_num_lenght = ir_values_obj.get_default('product.product', 'default_eq_prod_num_lenght')
        default_eq_seperator = ir_values_obj.get_default('product.product', 'default_eq_seperator')
        return {
            'default_eq_min_prefix_count': default_eq_min_prefix_count,
            'default_eq_max_prefix_count': default_eq_max_prefix_count,
            'default_eq_prod_num_lenght': default_eq_prod_num_lenght,
            'default_eq_seperator': default_eq_seperator,
        }

    default_eq_min_prefix_count = fields.Integer('Min prefix lenght [equitania]')
    default_eq_max_prefix_count = fields.Integer('Max prefix lenght [equitania]')
    default_eq_prod_num_lenght = fields.Integer('Product number lenght [equitania]')
    default_eq_seperator = fields.Char('Seperator [equitania]')
