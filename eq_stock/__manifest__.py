# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Equitania Lager Optimierungen',
    'license': 'AGPL-3',
    'version': '1.0.30',
    'description': """
        Erweiterung für Lager
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base', 'base_setup','delivery', 'stock','eq_base_report'],
    'category' : 'stock',
    'summary': 'Equitania Lager Erweiterung',

    'data': [
        "security/ir.model.access.csv",
        "data/eq_stock_incoterms_data.xml",
        "views/eq_stock_move_views.xml",
        "views/stock_picking_view.xml",
        "views/eq_stock_pack_operation_view.xml",
        "views/report_stock_barcode.xml",
        "views/report_stock_picking.xml",
        "views/report_stock_picking_packaging.xml",
    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
