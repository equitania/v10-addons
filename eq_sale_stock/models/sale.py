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



# TODO: umsetzen/ggf. verschieben sobald Erweiterung VEP-78 freigegeben wurde
class eq_sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    # def _get_delivery_date(self, cr, uid, ids, field_name, arg, context):
    #     result = {}
    #     for order_line in self.browse(cr, uid, ids, context):
    #         if order_line.order_id.show_delivery_date and order_line.eq_delivery_date:
    #             delivery_date = datetime.strptime(order_line.eq_delivery_date, OE_DFORMAT)
    #             if order_line.order_id.partner_id.eq_delivery_date_type_sale:
    #                 if order_line.order_id.partner_id.eq_delivery_date_type_sale == 'cw':
    #                     result[order_line.id] = 'KW ' + delivery_date.strftime('%V/%Y')
    #                 elif order_line.order_id.partner_id.eq_delivery_date_type_sale == 'date':
    #                     result[order_line.id] = delivery_date.strftime('%d.%m.%Y')
    #             else:
    #                 if order_line.order_id.use_calendar_week:
    #                     result[order_line.id] = 'KW ' + delivery_date.strftime('%V/%Y')
    #                 else:
    #                     result[order_line.id] = delivery_date.strftime('%d.%m.%Y')
    #         else:
    #             result[order_line.id] = False
    #
    #     return resul

    eq_delivery_date = fields.Date('Delivery Date')

