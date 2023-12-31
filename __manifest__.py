# -*- coding: utf-8 -*-
{
    'name': "Goals Sales Team",
    'summary': """
        Module that adds progress bars in sales teams, showing quotes, sales, invoiced and paid goals.""",
    'description': """
        Module that adds progress bars in sales teams, showing quotes, sales, invoiced and paid goals.
    """,
    'author': "Gt Alchemy Development",
    'license': 'LGPL-3',
    'support': 'developmentalchemygx@gmail.com',
    'category': 'Sales',
    'version': '0.1',
    'price': 2.00,
    'currency': 'USD',
    'depends': ['base','crm','sale','sales_team'],
    'data': [
        'data/data.xml',
        'views/crm_team_views.xml',
    ],
}