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

{
    'name': 'Equitania Website Product Block',
    'license': 'AGPL-3',
    'version': '1.0.1',
    'description': "Fügt einen Bereich für Produktbeschreibungen in der Produktdetailansicht hinzu",
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup', 'website_sale'],
    'category' : 'website sale',
    'summary': 'Fügt einen Bereich für Produktbeschreibungen in der Produktdetailansicht hinzu',

    'data': [
        "templates.xml",
    ],
    'demo': [],
    'css': ['base.css'],
    'active': False,
    'installable': True,
    'auto_install': False,
}
