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

from datetime import datetime, timedelta
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp
from openerp import workflow

class eq_framework_agreement(osv.osv):
    _name = "eq_framework_agreement"
    _rec_name = "eq_fa_number"

    def copy(self, cr, uid, id, default=None, context=None):
        new_no = self.env['ir.sequence'].get('eq_fa_sale.seq')
        default.update({
            'eq_fa_number': new_no,
        })
        return super(eq_framework_agreement, self).copy(cr, uid, id, default, context)


    def _get_amount_total(self, cr, uid, ids, field, arg, context=None):
        res = {}
        tax_obj = self.env['account.tax']
        for fa in self.browse(cr, uid, ids, context=context):
            untaxed = 0
            tax = 0
            total = 0
            for line in fa.eq_pos_ids:
                vals = tax_obj.compute_all(cr, uid, line.eq_tax_id, line.eq_sale_price, line.eq_quantity)
                total += vals['total_included']
                untaxed += vals['total']
                tax += vals['total_included'] - vals['total']
            res[fa.id] = {}
            res[fa.id]['eq_amount_untaxed'] = untaxed
            res[fa.id]['eq_amount_tax'] = tax
            res[fa.id]['eq_amount_total'] = total
        return res


    eq_fa_number = fields.Char('Framework Agreement No.', size=64),
    company_id = fields.Many2one('res.company', 'Company', required=False),
    eq_start_date = fields.Date('Start Date', required=True),
    eq_end_date = fields.Date('End Date', required=True),
    eq_contact_person_id = fields.Many2one('hr.employee', 'Sale Person'),
    eq_sale_person_id = fields.Many2one('res.users', 'Processor', required=True),
    eq_customer_id = fields.Many2one('res.partner', 'Customer', required=True),
    eq_invoice_address_id = fields.Many2one('res.partner', 'Dif. Invoice Address'),
    eq_delivery_address_id = fields.Many2one('res.partner', 'Dif. Delivery Address'),
    eq_customer_name = fields.Related('eq_customer_id', 'name', type='char', size=128, readonly=True),
    eq_street = fields.Related('eq_customer_id', 'street', type='char', size=128, readonly=True),
    eq_street2 = fields.Related('eq_customer_id', 'street2', type='char', size=128, readonly=True),
    eq_city = fields.Related('eq_customer_id', 'city', type='char', size=128, readonly=True),
    eq_zip = fields.Related('eq_customer_id', 'zip', type='char', size=24, readonly=True),
    eq_country_id = fields.Related('eq_customer_id', 'country_id', type='many2one', relation='res.country', string='Country', readonly=True),
    eq_ref = fields.Related('eq_customer_id', 'ref', type='char', size=24, readonly=True, string="Customer Number"),
    eq_info = fields.Html('Info'),
    eq_pos_ids = fields.One2many('eq_framework_agreement.pos', 'eq_agreement_id', 'Position', required=True),
    eq_product_id = fields.Related('eq_pos_ids', 'eq_product_id', type='many2one', relation='product.product', string='Product'),
    eq_amount_untaxed = fields.Function(_get_amount_total, multi="sum", type='float', string="Amount Untaxed"),
    eq_amount_tax = fields.Function(_get_amount_total, multi="sum", type='float', string="Amount Tax"),
    eq_amount_total = fields.Function(_get_amount_total, multi="sum", type='float', string="Amount Total"),
    eq_payment_term = fields.Many2one('account.payment.term', string='Payment Term'),
    eq_incoterm = fields.Many2one('stock.incoterms', string='Incoterm'),
    eq_delivery_condition = fields.Many2one('eq.delivery.conditions', string='Delivery Condition'),

    
    _defaults = {
        'company_id': lambda s, cr, uid, c: s.pool.get('res.company')._company_default_get(cr, uid, 'eq_framework_agreement', context=c),
                }
    
    _sql_constraints = [
                        ('eq_fa_number_unique', 'unique(eq_fa_number)', "This Framework Agreement Number is already used!")
                       ]
    
    def onchange_customer_id(self, cr, uid, ids, eq_customer_id, context=None):
        res = {'value': {}}
        current_customer = self.pool.get('res.partner').browse(cr, uid, eq_customer_id, context)
        if current_customer.eq_default_delivery_address:
            res['value']['eq_delivery_address_id'] = current_customer.eq_default_delivery_address.id
        if current_customer.eq_default_invoice_address:
            res['value']['eq_invoice_address_id'] = current_customer.eq_default_invoice_address.id
        if current_customer.eq_incoterm:
            res['value']['eq_incoterm'] = current_customer.eq_incoterm.id
        if current_customer.eq_deliver_condition_id:
            res['value']['eq_delivery_condition'] = current_customer.eq_deliver_condition_id.id
        if current_customer.property_payment_term:
            res['value']['eq_payment_term'] = current_customer.property_payment_term.id
        return res
    
    def create(self, cr, uid, vals, context):
        if not vals.get('eq_fa_number', False):
            vals['eq_fa_number'] = self.pool.get('ir.sequence').get(cr, uid, 'eq_fa_sale.seq')
        return super(eq_framework_agreement, self).create(cr, uid, vals, context)
        
    
    def create_offer(self, cr, uid, ids, context):
        offer_pos_vals = {}
        """
        for pos_id in eq_pos_ids:
            pos = self.pool.get('eq_framework_agreement.pos').read()
        """
        
        fq = self.pool.get('eq_framework_agreement').browse(cr, uid, ids, context)
        fa_pos_id = fq.eq_pos_ids
        #Sets User id
        user_id = fq.eq_sale_person_id.id
        contact_person = False
        if fq.eq_contact_person_id:
            contact_person = fq.eq_contact_person_id.id
        #Sale Order values
        offer_vals = {
                'name': self.pool.get('ir.sequence').get(cr, uid, 'sale.order'),                 
                'company_id': fq.company_id.id,
                'partner_id': context.get('eq_customer_id'),
                'warehouse_id': 1,
                'client_order_ref': context.get('eq_ref'),
                'note': context.get('eq_info'),
                'user_id': user_id,
                'eq_contact_person_id': contact_person,
                'incoterm': fq.eq_incoterm.id,
                'eq_deliver_condition_id': fq.eq_delivery_condition.id,
                'payment_term': fq.eq_payment_term.id,
                'eq_framework_agreement_id': fq.id, #id rahmenauftrag
                }
        
        if fq.eq_invoice_address_id:
            offer_vals['partner_invoice_id'] = fq.eq_invoice_address_id.id
        if fq.eq_delivery_address_id:
            offer_vals['partner_delivery_id'] = fq.eq_delivery_address_id.id
        #Creates the Offer
        offer_id = self.pool.get('sale.order').create(cr, uid, offer_vals, context)
        seq = 10
        for position in fa_pos_id:
            delay = position.eq_product_id.sale_delay
            eq_delivery_date = False
            if delay:
                date_order = datetime.today()
                eq_delivery_date = date_order + timedelta(days=int(delay))
            #Position values
            pos = {
                    'sequence': seq,
                    'name': position.eq_product_id.description_sale if position.eq_product_id.description_sale else position.eq_product_id.name,
                    'company_id': fq.company_id.id,
                    'eq_delivery_date': eq_delivery_date,
                    'product_id': position.eq_product_id.id,
                    'price_unit': position.eq_sale_price,
                    'product_uom_qty': position.eq_min_purch_qua,
                    'order_id': offer_id,
                    'eq_agreement_id': ids[0],
                    }
            if position.eq_tax_id:
                pos['tax_id'] = [(6, 0, [position.eq_tax_id.id])],
            seq = seq + 10
            #Creates Positions
            pos_id = self.pool.get('sale.order.line').create(cr, uid, pos, context)
        #Returns the form view of the created Sale Order
        mod_obj = self.pool.get('ir.model.data')
        res = mod_obj.get_object_reference(cr, uid, 'sale', 'view_order_form')
        return {
            'name': 'Offer',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [res and res[1] or False],
            'res_model': 'sale.order',
            'context': "{}",
            'type': 'ir.actions.act_window',
            'nodestroy': False,
            'target': 'current',
            'res_id': offer_id or False,
        }
        
    """Only one id at a time"""
    def eq_fa_update(self, cr, uid, ids, context={}):
        current_fa = self.browse(cr, uid, ids, context)
        if not current_fa[0].eq_fa_number:
            vals = {
                    'eq_fa_number': self.pool.get('ir.sequence').get(cr, uid, 'eq_fa_sale.seq'),
                    }
            self.write(cr, uid, ids, vals, context=context)
    
eq_framework_agreement()

class eq_framework_agreement_pos(osv.osv):    
    _name = "eq_framework_agreement.pos"
    _rec_name = "eq_product_id"
    
    def _calc_quantity(self, cr, uid, ids, field_name, arg, context=None): 
        res = {}       
        for pos in self.browse(cr, uid, ids, context=context):
            res[pos.id] = {
                   'eq_ordered_qua': 0.0,
                   'eq_quantity_delivered': 0.0,
                   'eq_qua_left': pos.eq_quantity,
                   }
            if self.browse(cr, uid, pos.id).eq_pos_fetches_ids:
                for fetches in self.browse(cr, uid, pos.id).eq_pos_fetches_ids:
                    res[pos.id]['eq_ordered_qua'] += fetches.eq_quantity
                    delivered = sum([move.product_uom_qty if move.state == 'done' else 0 for move in fetches.eq_stock_moves_delivered])
                    res[pos.id]['eq_quantity_delivered'] += delivered
                    res[pos.id]['eq_qua_left'] -= fetches.eq_quantity if fetches.eq_quantity >= delivered and not fetches.eq_done or fetches.eq_quantity < 0 else delivered
        return res
    
    def _get_subtotal(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = line.eq_quantity * line.eq_sale_price
        return res

    

    eq_product_id = fields.Many2one('product.product', 'Product', required=True),
    eq_quantity = fields.Float('Quantity', required=True),
    eq_min_purch_qua = fields.Float('Min. Purchase Quantity', required=True),
    eq_ordered_qua = fields.Function(_calc_quantity, arg=None, type="float", method=True, store=False,
                                digits_compute=dp.get_precision('Sale Price'), string="Ordered Quantity", multi="quantity", readonly=True),
    eq_qua_left = fields.Function(_calc_quantity, arg=None, type="float", method=True, store=False,
                                digits_compute=dp.get_precision('Sale Price'), string="Quantity left", multi="quantity", readonly=True),
    eq_quantity_delivered = fields.Function(_calc_quantity, arg=None, type="float", method=True, store=False,
                                digits_compute=dp.get_precision('Sale Price'), string="Quantity delivered", multi="quantity", readonly=True),
    eq_sale_price = fields.Float('Sale Price', required=True),
    eq_agreement_id = fields.Many2one('eq_framework_agreement', 'Framework Agreement', select=True, invisible=True, readonly=True),
    eq_pos_fetches_ids = fields.One2many('eq_framework_agreement.pos.fetches', 'eq_pos_id', 'Fetches', readonly=True),
    eq_tax_id = fields.Many2one('account.tax', string='Tax'),
    eq_subtotal = fields.Function(_get_subtotal, type='float', string="Subtotal"),


eq_framework_agreement_pos()

class eq_framework_agreement_pos_fetches(osv.osv):    
    _name = "eq_framework_agreement.pos.fetches"
    _rec_name = "eq_pos_id"
    
    def compute_delivered_qty(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for fetch in self.browse(cr, uid, ids, context):
            res[fetch.id] = sum([move.product_uom_qty for move in fetch.eq_stock_moves_delivered])
        return res
    

    eq_quantity = fields.Float('Quantity'),
    eq_delivered_quantity = fields.Function(compute_delivered_qty, type="float", method=True, store=False, string="Delivered Qty"),
    eq_pos_id = fields.Many2one('eq_framework_agreement.pos', 'Product'),
    eq_order_ref = fields.Many2one('sale.order', 'Sale Order'),
    eq_stock_moves_delivered = fields.One2many('stock.move', 'eq_fa_fetch_id', string="Stock moves"),
    eq_done = fields.Boolean('Finished'),

    
    _defaults = {
                 'eq_done': False,
                 }

eq_framework_agreement_pos_fetches()

class eq_framework_agreement_order(osv.osv):
    _inherit = "sale.order"
    
    def action_cancel(self, cr, uid, ids, context):
        #Create a reverse fetch if the line has a fetch. 
        order = self.browse(cr, uid, ids, context)
        for line in order.order_line:
            if line.eq_pos_fetch_id:
                values = {
                          'eq_quantity': -(line.eq_pos_fetch_id.eq_quantity),
                          'eq_pos_id': line.eq_pos_fetch_id.eq_pos_id.id,
                          'eq_order_ref': line.eq_pos_fetch_id.eq_order_ref.id,
                          }
                self.pool.get('eq_framework_agreement.pos.fetches').create(cr, uid, values)
        return super(eq_framework_agreement_order,self).action_cancel(cr, uid, ids, context)
            
    def action_button_confirm(self, cr, uid, ids, context=None):
        #Creates the fetch.
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        self.signal_workflow(cr, uid, ids, 'order_confirm')
        for line in self.browse(cr, uid, ids, context).order_line:
            if line.eq_agreement_id:
                pos_id = self.pool.get('eq_framework_agreement.pos').search(cr, uid, [('eq_agreement_id', '=', line.eq_agreement_id.id), ('eq_product_id', '=', line.product_id.id)])
                fetch_vals = {
                              'eq_quantity': line.product_uom_qty,
                              'eq_pos_id': pos_id[0] if pos_id else False,
                              'eq_order_ref': ids[0],
                              }
                
                fetch_id = self.pool.get('eq_framework_agreement.pos.fetches').create(cr, uid, fetch_vals)
                values = {}
                values['eq_pos_fetch_id'] = fetch_id
                self.pool.get('sale.order.line').write(cr, uid, line.id, values)
        return True
        
eq_framework_agreement_order()

class eq_framework_agreement_order_line(osv.osv):
    _inherit = 'sale.order.line'
     

    eq_agreement_id = fields.Many2one('eq_framework_agreement', 'FA', help="Framework Agreement", readonly=True, states={'draft': [('readonly', False)]}),
    eq_pos_fetch_id = fields.Many2one('eq_framework_agreement.pos.fetches', 'Fetch'),

    
    def _get_uos_id(self, cr, uid, *args):
        try:
            proxy = self.pool.get('ir.model.data')
            result = proxy.get_object_reference(cr, uid, 'product', 'product_uom_unit')
            return result[1]
        except Exception, ex:
            return False
        
    _defaults = {
                'product_uos': _get_uos_id,
                 }
    
    def on_change_fa(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, eq_fa=False, context=None):
        if not eq_fa:
            try:
                res = super(eq_framework_agreement_order_line, self).product_id_change_with_wh(cr, uid, ids, pricelist, product, qty,
                                                               uom, qty_uos, uos, name, partner_id,
                                                               lang, update_tax, date_order, packaging, fiscal_position, flag, context)
            except:
                res = super(eq_framework_agreement_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty,
                                                               uom, qty_uos, uos, name, partner_id,
                                                               lang, update_tax, date_order, packaging, fiscal_position, flag, context)
            return res
    
    #If the product is in an Frameworkagreement, it fills the apropriate fields.
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        
        result = super(eq_framework_agreement_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty,
                                                               uom, qty_uos, uos, name, partner_id,
                                                               lang, update_tax, date_order, packaging, fiscal_position, flag, context)
                
        """
            small workaround for our little problem with offers
            no offer should be linked to one/many framework agreement(s), otherwise stick with this functionality to
            make sure, that everything will be checked            
        """
        
        # small bugfix for our exceltool
        if context is not None:
            if context.get('eq_calculationflag') is None:   
                #Addition from custom Modul. Adds the Order line Data.
                any_fa_product = False
                line = self.browse(cr, uid ,ids)
                message = []
                if partner_id:
                    fr_agr_ids = self.pool.get('eq_framework_agreement', self).search(cr, uid, ['&', '&',('eq_customer_id.id', '=', partner_id), ('eq_start_date', '<=', datetime.now()), ('eq_end_date', '>=', datetime.now()), ])
                    fr_agr_ids.sort(reverse=True)
                    if fr_agr_ids:
                        fr_agreements = self.pool.get('eq_framework_agreement').browse(cr, uid, fr_agr_ids, context)
                        for fr_agr in fr_agreements:
                            for position in fr_agr.eq_pos_ids:
                                if product == position.eq_product_id.id and position.eq_qua_left > 0:
                                    if qty > position.eq_qua_left + line.eq_pos_fetch_id.eq_quantity or qty < position.eq_min_purch_qua + line.eq_pos_fetch_id.eq_quantity:
                                        message.append((
                                                        position.eq_agreement_id.eq_fa_number, 
                                                        position.eq_qua_left, 
                                                        position.eq_product_id.uom_id.name,
                                                        position.eq_min_purch_qua, 
                                                        position.eq_product_id.uom_id.name,
                                                        position.eq_sale_price))
                                    else:
                                        result['value']['price_unit'] = position.eq_sale_price
                                        result['value']['eq_agreement_id'] = position.eq_agreement_id
                                        any_fa_product = True
                if not any_fa_product:
                    result['value']['eq_agreement_id'] = False
                else:
                    message = []
                result['message_vals'] = message
        return result #{'value': result, 'domain': domain, 'warning': warning} <-- result
    
    #shows the warning messages for the framework agreement
    def product_id_change_with_wh(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, warehouse_id=False, show_msg=False, context=None):
        
        result = super(eq_framework_agreement_order_line, self).product_id_change_with_wh(cr, uid, ids, pricelist, product, qty,
            uom, qty_uos, uos, name, partner_id,
            lang, update_tax, date_order, packaging, fiscal_position, flag, warehouse_id, context)
        
        #Creates the error message with all the available framework agreements
        if 'message_vals' in result and len(result['message_vals']) and not update_tax:
            message_head = _("The following framework agreements are available.\n")
            message_body_rep = _("\nFA Number: %s\nQuantity Left: %s %s\nMin Qty: %s %s\nSale price: %s")
            message_body = "".join([message_body_rep % message_vals for message_vals in result['message_vals']])
            result['warning'] = {
                                 'title': _('Framework Agreement'),
                                 'message' : (message_head + message_body),
                                 }
            del result['message_vals']
        return result

eq_framework_agreement_order_line()

class eq_stock_move(osv.osv):
    _inherit = 'stock.move'
    

    eq_fa_fetch_id = fields.Many2one('eq_framework_agreement.pos.fetches', 'Framework Agreement Fetch', copy=False)

    
    def action_done(self, cr, uid, ids, context=None):
        """ Runs the actual method and adds the move to the framework agreement fetch.
        """
        res = super(eq_stock_move, self).action_done(cr, uid, ids, context=context)
        
        for move in self.browse(cr, uid, ids, context=context):
            if move.procurement_id:
                if move.procurement_id.sale_line_id:
                    if move.procurement_id.sale_line_id.eq_pos_fetch_id and move.picking_id:
                        self.write(cr, uid, move.id, {'eq_fa_fetch_id': move.procurement_id.sale_line_id.eq_pos_fetch_id.id})
                        if move.procurement_id.state == 'done':
                            self.pool.get('eq_framework_agreement.pos.fetches').write(cr, uid, move.procurement_id.sale_line_id.eq_pos_fetch_id.id, {'eq_done': True})
                    
        return res
    
    
    def action_cancel(self, cr, uid, ids, context=None):
        res = super(eq_stock_move, self).action_cancel(cr, uid, ids, context=context)       
        for move in self.browse(cr, uid, ids, context=context):
            if move.procurement_id:
                if move.procurement_id.sale_line_id:
                    if move.procurement_id.sale_line_id.eq_pos_fetch_id and move.picking_id:
                        self.write(cr, uid, move.id, {'eq_fa_fetch_id': move.procurement_id.sale_line_id.eq_pos_fetch_id.id})
                        if move.procurement_id.state == 'cancel':
                            self.pool.get('eq_framework_agreement.pos.fetches').write(cr, uid, move.procurement_id.sale_line_id.eq_pos_fetch_id.id, {'eq_done': True})
        return res