# -*- coding: utf-8 -*-

from odoo import api, models, _
from odoo.exceptions import ValidationError


class EqFooterReport(models.AbstractModel):
    _name = 'report.eq_base_report.eq_external_layout_footer'

    @api.model
    def render_html(self, docids, data=None):
        company_partner = None
        ceo = None
        company = self.env.user.company_id

        if company:
            company_partner = company.partner_id
            ceo = company.ps_ceo

        vat = company.vat

        if self.env['res.partner.bank'].search_count(
                [('partner_id', '=', company_partner.id), ('company_id', '=', self.env.user.company_id.id),
                 ('ps_print_on_reports', '=', True)]) == 0:
            raise ValidationError(_('Please select exactly one bank account to be printed on the report.'))

        if self.env['res.partner.bank'].search_count(
                [('partner_id', '=', company_partner.id), ('company_id', '=', self.env.user.company_id.id),
                 ('ps_print_on_reports', '=', True)]) > 1:
            raise ValidationError(_('You can only select one bank account to be printed on the report.'))

        bank = self.env['res.partner.bank'].search(
            [('partner_id', '=', company_partner.id), ('company_id', '=', self.env.user.company_id.id),
             ('ps_print_on_reports', '=', True)])

        bank_iban = ''
        bank_bic = ''
        bank_name = ''

        if bank:
            bank_iban = bank.acc_number
            bank_bic = bank.bank_id.bic
            bank_name = bank.bank_id.name

        docargs = {
            'doc_ids': docids,
            'doc_model': 'account.invoice',
            'docs': None,
            'vat': vat,
            'bank_iban': _('IBAN: ') + bank_iban,
            'bank_bic': _('BIC: ') + bank_bic,
            'bank_name': bank_name,
            'ceo': ceo,
        }

        return self.env['report'].render('eq_base_report.eq_external_layout_footer', docargs)
