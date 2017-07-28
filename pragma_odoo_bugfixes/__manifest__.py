# -*- coding: utf-8 -*-


{
    'name': 'pragmasoft - Bugfixes for odoo',
    'version': '1.0.0',
    'category': 'Base',
    'description': """
        Fixes bugs in odoo which have not yet been fixed by odoo SA.
    """,
    'author': 'Josef Kaser',
    'website': 'http://www.pragmasoft.de',
    'depends': [
        'base',
        'sale',
        'purchase',
    ],
    'data': [
        'views/purchase_views.xml',
        # 'views/sale_views.xml',
    ],
    'installable': True,
    'active': False,
}
