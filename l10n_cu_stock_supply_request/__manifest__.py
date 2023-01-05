# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Supply request',
    'version' : '1.0',
    'summary': 'Import product from excel',
    'sequence': 30,
    'description': """
    This modulo allow create a Supply request

    """,
    'category': 'Stock',
    'website': 'http://www.desoft.cu',
    'author': "Desoft. Holguín. Cuba.",
    'images': [],
    'depends': ['stock',],
    'data': [
        'views/supply_request_view.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'wizard/import_invoice_wizard_view.xml',
        # 'wizard/import_account_wizard_view.xml',
        # 'wizard/import_payment_wizard_view.xml',
        # 'views/account_invoice_view.xml',
    ],
    'demo': [

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
