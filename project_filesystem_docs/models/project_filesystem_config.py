# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields

class project_filesystem_config(models.Model):
    name = 'project_filesystem_config'

    view_base_folder = fields.Char("Carpeta base de Proyectos para vista",default="//server/d")
    base_folder = fields.Char("Carpeta base de Proyectos para backend",default="/home/bitnami/mnt/serverd")
    cotizacion_folder = fields.Char("Carpeta de Cotización",default='/cotizaciones/enviadas')
    trabajos_folder = fields.Char("Carpeta de Trabajos",default='/trabajos')
    base_document_folder = fields.Char("Carpeta base de documentos",default='/cotizaciones/base')


    
