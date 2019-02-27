from odoo import models, fields, api, _

class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    eq_check_vat = fields.Boolean(string="Validate VAT")