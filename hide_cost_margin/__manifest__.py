# -*- coding: utf-8 -*-
{
    'name': "Hide Costs Fields",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','sale_margin'],

    # always loaded
    'data': [
        'security/security.xml',
        'views/cost_margin_rights.xml',

    ],

}
