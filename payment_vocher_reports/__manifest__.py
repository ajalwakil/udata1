# -*- coding: utf-8 -*-
{
    'name': "Payment Vocher Reports",
    'summary': """ """,
    'description': """ """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'account'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/payment_voucher.xml',
        'views/receipt_voucher.xml',
        # 'views/pdc_voucher.xml',
        'views/report.xml',
    ],
}
