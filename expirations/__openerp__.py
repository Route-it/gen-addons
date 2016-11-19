# -*- coding: utf-8 -*-
{
    'name': "expirations",

    'summary': """
        Permite administrar fechas de vencimiento, de manera sencilla con el calendario de odoo""",

    'description': """
        
    """,

    'author': "Route IT",
    'website': "http://www.routeit.com.ar",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Calendar',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','calendar'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/data.xml',
        'views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}