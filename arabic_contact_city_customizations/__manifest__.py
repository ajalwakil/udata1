# -*- coding: utf-8 -*-
{
    'name': "Arabic Contact City Customizations",
    'summary': """ """,
    'description': """ """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base','ksa_e_invoive'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/arabic_city.xml',
        'views/arabic_country.xml',
        'views/res_partner_view.xml',
    ],
}
