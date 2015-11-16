# -*- coding: utf-8 -*-
{
    'name': "Fleet Vehicle Planning",

    'summary': """
        Planificacion de vehiculos. Visualizacion en calendario y Gantt""",

    'description': """
        Planificacion de vehiculos.
    """,

    'author': "Route IT",
    'website': "http://www.routeit.com.ar",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Managing vehicles and contracts',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['fleet'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/fleet_vehicle_planning_view.xml',
        'views/menu.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}