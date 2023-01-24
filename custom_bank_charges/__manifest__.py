# -*- coding: utf-8 -*-
{
    'name': "Bank Charges",
    'summary': """ To Add Extra Bank Charges""",
    'description': """Bank Charges """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base','account','account_payment'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
