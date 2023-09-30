# -*- coding: utf-8 -*-
{
    'name': "Subscription Customizations",
    'summary': """ """,
    'description': """ """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base','sale_subscription'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/mail_template_data.xml',
        'views/views.xml',
    ],
}
