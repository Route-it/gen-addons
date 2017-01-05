# -*- coding: utf-8 -*-
{
    'name': "project_filesystem_docs",

    'summary': """
        Administra el filesystem para los documentos que pertenecen a un proyecto.""",

    'description': """
        Permite administrar una estructra de directorios y sus documentos 
        asociados a un proyecto.        
    """,

    'author': "Ing. Diego Richi",
    'website': "http://www.diegorichi.com.ar",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'project',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','project-genexa'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views_inherit.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}