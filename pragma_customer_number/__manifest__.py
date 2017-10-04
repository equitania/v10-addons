# -*- coding: utf-8 -*-
##############################################################################
#
#    odoo (formerly known as OpenERP), Open Source Business Applications
#    Copyright (C) 2012-now Josef Kaser (<http://www.pragmasoft.de>).
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
{
    "name": "pragmasoft - Customer Number",
    "version": "1.1.2",
    'author': 'Josef Kaser',
    'website': 'https://www.pragmasoft.de',
    "description": """
    Extends the customer number functionality.
    """,
    "category": "Customization",
    "depends": [
        "base",
        "sale",
    ],
    "data": [
        "views/partner_view.xml"
    ],
    "installable": True,
    "auto_install": False,
}
