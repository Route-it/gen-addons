# -*- coding: utf-8 -*-
{
    'name': "Genexa Project Management",
   'version': '0.1',
    'author': 'Route IT',
    'website': 'https://www.routeit.com.ar',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Project Management',
    'summary': """
        Extension del modulo de manejo de proyectos para cambiar el workflow y adecuarlo a la Genexa SRL
    """,

    'description': """
        Corresponde a la carpeta static.
    """,

    # any module necessary for this one to work correctly
    'depends': ['project'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'project_data.xml',
        'views/project_project_view.xml',
        'views/project_task_view.xml',
        'views/menu.xml'
    ],
    # only loaded in demonstration mode
    'demo': ['project_demo.xml'],
}