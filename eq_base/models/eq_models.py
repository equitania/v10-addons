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

original_search_read = models.BaseModel.search_read


class BaseModelExtend(models.AbstractModel):
    _name = 'basemodel.extend'

    def _register_hook(self):
        @api.model
        def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
            # alt
            # for dom in domain:
            #     if isinstance(dom, list) and isinstance(dom[2], str) and dom[2][0] == "|":
            #         dom[1] = "=ilike"
            #         dom[2] = dom[2][1:]
            # return original_search_read(self, cr, uid, domain, fields, offset, limit, order, context)

            new_dom = []
            empty_space_found = False
            for dom in domain:
                if isinstance(dom, list) and isinstance(dom[2], unicode):
                    if len(dom) > 2:
                        if len(dom[2]) > 0:
                            if dom[2][0] == "|":
                                dom[1] = "=ilike"
                                dom[2] = dom[2][1:]
                            elif ' ' in dom[2] and isinstance(dom[2], str):
                                empty_space_found = True
                                split_condition = dom[2].split(' ')
                                for _ in range(0, len(split_condition) - 1):
                                    new_dom.append('&')
                                for cond in split_condition:
                                    # new_dom.append(dom)
                                    new_dom.append([dom[0], 'ilike', cond])
                                continue

                new_dom.append(dom)
            if empty_space_found:
                return original_search_read(self, new_dom, fields, offset, limit, order)
            else:
                return original_search_read(self, domain, fields, offset, limit, order)

        models.BaseModel.search_read = search_read

        return super(BaseModelExtend, self)._register_hook()