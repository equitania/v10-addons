# -*- coding: utf-8 -*-
{
    'name': 'pragmasoft - Automatic Account Creation',
    'description': """
Create debitor and creditor account automatically when creating a customer/supplier. Can set the account number as
customer/supplier number.

Functionality:

-    When "Customer" is set an account with the name of the customer is being created and assigned.
-    When "Supplier" is set an account with the name of the supplier is being created and assigned.
-    When "Customer" or "Supplier" is set a customer and/or supplier number is being created from a sequencer.
    
Available settings (in "Accounting - Settings"):

-    Enable/disable the automatic account creation.
  """,
    'version': '1.3',
    'author': 'Josef Kaser',
    'category': 'Localization',
    'website': 'https://www.pragmasoft.de',
    'depends': [
        'base',
        'base_setup',
        'account',
        'pragma_customer_number',
        'pragma_supplier_number',
        'pragma_odoo_bugfixes',
    ],
    'data': [
        "views/base_config_settings_view.xml",
        "views/partner_view.xml",
        "data/sequencer.xml"
    ],
    'test': [
    ],
    'installable': True,
}
