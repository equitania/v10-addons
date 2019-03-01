from odoo import models, fields, api, _

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    eq_layout_category_id = fields.Many2one('sale.layout_category', string='Section')