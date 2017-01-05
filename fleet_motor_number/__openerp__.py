# -*- coding: utf-8 -*-
{
    'name': "Numero de motor",
    'version': '0.1',
    'author': "Ing. Diego Richi",
    'website': "http://www.diegorichi.com.ar",

    'summary': """
        Agrega el nro de motor para los vehiculos""",

    'description': """
        agrega el campo numero de motor a los vehiculos.
    """,



    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Human Resources',

    # any module necessary for this one to work correctly
    'depends': ['fleet'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/fleet_views.xml',
    ],
}