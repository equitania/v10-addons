# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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