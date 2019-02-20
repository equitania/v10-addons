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

class eq_res_partner(models.Model):

    _inherit = 'res.partner'


    eq_firstname = fields.Char('Firstname')
    eq_name2 = fields.Char('Name2')
    eq_name3 = fields.Char('Name3')

    eq_house_no = fields.Char('House number')
    eq_citypart = fields.Char('District')
    eq_birthday = fields.Date('Birthday')
    eq_letter_salutation = fields.Char('Salutation')
    eq_foreign_ref = fields.Char('Foreign reference')
    eq_foreign_ref_purchase = fields.Char('Foreign reference purchase')

    eq_email2 = fields.Char('E-Mail (additional)')
    eq_phone2 = fields.Char('Phone (additional)')

    eq_deb_cred_number = fields.Char(compute="_show_deb_cred_number", store=False)

    customer_number = fields.Char(string=_('Customer Number'))
    supplier_number = fields.Char(string=_('Supplier Number'))

    eq_custom1 = fields.Char(string='Freefield (1)', size=100)
    eq_custom2 = fields.Char(string='Freefield (2)', size=100)
    eq_custom3 = fields.Char(string='Freefield (3)', size=100)


    #eq_complete_description = fields.Char(compute='_generate_complete_description', store=True)

    @api.multi
    def _fields_sync(self, values):
        """ Sync commercial fields and address fields from company and to children after create/update,
        just as if those were all modeled as fields.related to the parent """
        # 1. From UPSTREAM: sync from parent
        if values.get('parent_id') or values.get('type', 'contact'):
            # 1a. Commercial fields: sync if parent changed
            if values.get('parent_id'):
                self._commercial_sync_from_company()
            # 1b. Address fields: sync if parent or use_parent changed *and* both are now set
            if self.parent_id and self.type == 'contact':
                onchange_vals = self.onchange_parent_id().get('value', {})
                self.update_address(onchange_vals)

        # 2. To DOWNSTREAM: sync children
        if self.child_ids:
            # 2a. Commercial Fields: sync if commercial entity
            if self.commercial_partner_id == self:
                commercial_fields = self._commercial_fields()
                if any(field in values for field in commercial_fields):
                    self._commercial_sync_to_children()
            for child in self.child_ids.filtered(lambda c: not c.is_company):
                if child.commercial_partner_id != self.commercial_partner_id:
                    self._commercial_sync_to_children()
                    break
            # 2b. Address fields: sync if address changed
            address_fields = self._address_fields()
            if any(field in values for field in address_fields):
                contacts = self.child_ids.filtered(lambda c: c.type == 'contact')
                for contact in contacts:
                    if contact.street == '' or contact.street == None or contact.street == False:
                        contact.update_address(values)

    @api.onchange('parent_id')
    def _onchange_parent_id(self):
        # onchange function which changes the value of customer_number which depends from parent_id
        if self.parent_id:
            if self.parent_id.customer_number:
                self.customer_number = self.parent_id.customer_number


    @api.onchange('parent_id')
    def onchange_parent_id(self):
        # return values in result, as this method is used by _fields_sync()
        if not self.parent_id:
            return
        result = {}
        partner = getattr(self, '_origin', self)
        if partner.parent_id and partner.parent_id != self.parent_id:
            result['warning'] = {
                'title': _('Warning'),
                'message': _('Changing the company of a contact should only be done if it '
                             'was never correctly set. If an existing contact starts working for a new '
                             'company then a new contact should be created under that new '
                             'company. You can use the "Discard" button to abandon this change.')}
        if partner.type == 'contact' or self.type == 'contact':
            if partner.street == '' or partner.street == None or partner.street == False:
                # for contacts: copy the parent address, if set (aka, at least one
                # value is set in the address: otherwise, keep the one from the
                # contact)
                address_fields = self._address_fields()
                if any(self.parent_id[key] for key in address_fields):
                    def convert(value):
                        return value.id if isinstance(value, models.BaseModel) else value
                    result['value'] = {key: convert(self.parent_id[key]) for key in address_fields}
        return result

    @api.model
    def _address_fields(self):
        res = super(eq_res_partner, self)._address_fields()
        res.extend(("eq_house_no", "eq_citypart"))
        return res


    @api.multi
    def _show_deb_cred_number(self):
        """
        Setzen des Feldes für die Anzeige der Kunden- und Lieferantennr in der Kanbanview
        :return:
        """
        for partner in self:
            deb_cred = False
            if partner.customer_number != 'False' and partner.customer_number and partner.supplier_number != 'False' and partner.supplier_number:
                deb_cred = partner.customer_number + ' / ' + partner.supplier_number
            elif partner.customer_number != 'False' and partner.customer_number:
                deb_cred = partner.customer_number
            elif partner.supplier_number != 'False' and partner.supplier_number:
                deb_cred = partner.supplier_number
            partner.eq_deb_cred_number = deb_cred

    @api.model
    def create(self, vals):
        """
        Createhandler
        :param vals: All posted data
        :return: Result of call of super method
        """
        for obj in self:
            if obj.parent_id:
                if obj.parent_id.customer_number:
                    vals.update({'customer_number': obj.parent_id.customer_number})

        res = super(eq_res_partner, self).create(vals)

        for object in self:
            if object.parent_id:
                if not object.type:
                    object.type = 'contact'
        return res

    @api.multi
    def write(self, vals):
        """
        Updatehandler
        :param vals: All posted data
        :return: Result of call of super method
        """
        
        # Commented on 17.12.2018 after meeting with Julia and Robin
        # for obj in self:
        #     if obj.parent_id:
        #         if obj.parent_id.customer_number:
        #             vals.update({'customer_number': obj.parent_id.customer_number})

        res = super(eq_res_partner, self).write(vals)

        for object in self:
            if object.parent_id:
                if not object.type:
                    object.type = 'contact'
        return res
    
    @api.depends('is_company', 'name', 'parent_id.name', 'type', 'company_name', 'eq_firstname')
    def _compute_display_name(self):
        diff = dict(show_address=None, show_address_only=None, show_email=None)
        names = dict(self.with_context(**diff).name_get())
        for partner in self:
            partner.display_name = names.get(partner.id)