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
from openerp import models, fields, api
from os.path import os
import shutil

class project_project(models.Model):
    _inherit = 'project.project'

    project_folder = fields.Char("Carpeta del proyecto para backend",compute='compute_project_folder')
    cotizacion_folder = fields.Char("Carpeta de cotización para backend",compute='compute_cotizacion_folder')
    view_project_folder = fields.Char("Carpeta del proyecto",compute='compute_view_project_folder')
    view_cotizacion_folder = fields.Char("Carpeta de cotización",compute='compute_view_cotizacion_folder')

    project_folder_exist = fields.Boolean('Existe carpeta de proyecto',compute='compute_project_folder_exist')
    cotizacion_folder_exist = fields.Boolean('Existe carpeta de cotizacion',compute='compute_cotizacion_folder_exist')
    base_doc_folder_exist = fields.Boolean('Existe carpeta de documentos base',compute='compute_base_doc_folder_exist')

    project_filesystem_config = fields.Many2one('project_filesystem_config',compute='compute_project_filesystem_config')

    @api.one
    def compute_project_filesystem_config(self):
        pfsc = self.project_filesystem_config or False
        if not pfsc:
            self.project_filesystem_config = self.env['project_filesystem_config'].browse(1)
        
    @api.one
    def compute_base_doc_folder_exist(self):
        pfc = self.project_filesystem_config or False
        if pfc != False:
            pfcdf = pfc.base_folder + pfc.base_document_folder +'/'+ self.type_project_id.code
            self.base_doc_folder_exist = os.path.exists(pfcdf)
        
    @api.one
    def compute_project_folder_exist(self):
        self.project_folder_exist = os.path.exists(self.project_folder)
        
    @api.one
    def compute_cotizacion_folder_exist(self):
        self.cotizacion_folder_exist = os.path.exists(self.cotizacion_folder)
        
    @api.one
    def compute_project_folder(self):
        pfc = self.project_filesystem_config or False
        base = ''
        trabajos = ''
        if pfc:
            base = pfc.base_folder
            trabajos = pfc.trabajos_folder

        proy = self.nombre_completo
        year = self.start_date[0:4]
        state_folder = 'abiertos'
        if (self.state == 'terminar' or self.state == 'cobrar'):
                state_folder = 'terminados para cobrar'
        else: 
            if (self.state == 'cerrado'):
                state_folder = 'cerrados'
            
        self.project_folder = base +trabajos+'\\'+ str(year) +'\\'+ state_folder +'\\' + proy

    @api.one
    def compute_view_project_folder(self):
        pfc = self.project_filesystem_config or False
        base = ''
        trabajos = ''
        if pfc:
            base = pfc.view_base_folder
            trabajos = pfc.trabajos_folder

        proy = self.nombre_completo
        year = self.start_date[0:4]
        state_folder = 'abiertos'
        if (self.state == 'terminar' or self.state == 'cobrar'):
                state_folder = 'terminados para cobrar'
        else: 
            if (self.state == 'cerrado'):
                state_folder = 'cerrados'
            
        self.view_project_folder = os.path.abspath(base +trabajos+'\\'+ str(year) +'\\'+ state_folder +'\\' + proy)

        
    @api.one
    def compute_view_cotizacion_folder(self):
        pfc = self.project_filesystem_config or False
        base = ''
        cotizacion = ''
        if pfc:
            base = pfc.view_base_folder
            cotizacion = pfc.cotizacion_folder

        proy = self.nombre_completo
        year = self.start_date[0:4]
        self.view_cotizacion_folder = os.path.abspath(base + cotizacion+'\\'+ str(year) +'\\' + proy)

    @api.one
    def compute_cotizacion_folder(self):
        pfc = self.project_filesystem_config or False
        base = ''
        cotizacion = ''
        if pfc:
            base = pfc.base_folder
            cotizacion = pfc.cotizacion_folder

        proy = self.nombre_completo
        year = self.start_date[0:4]
        self.cotizacion_folder = base + cotizacion+'\\'+ str(year) +'\\' + proy
    
    @api.multi
    def create_project_folder(self):
        if not self.project_folder_exist:
            os.makedirs(self.project_folder)

    @api.multi
    def create_cotizacion_folder(self):
        if not self.cotizacion_folder_exist:
            os.makedirs(self.cotizacion_folder)

    @api.multi
    def copy_documents(self):
        pfc = self.project_filesystem_config or False
        if pfc != False:
            pfcdf = pfc.base_folder + pfc.base_document_folder +'/'+ self.type_project_id.code
            if self.cotizacion_folder_exist:
                if os.path.exists(self.cotizacion_folder+'/Documentos_base'):
                    shutil.rmtree(self.cotizacion_folder+'/Documentos_base', True)
                shutil.copytree(pfcdf,self.cotizacion_folder+'/Documentos_base', symlinks=False, ignore=None)
            else: 
                if self.project_folder_exist:
                    if os.path.exists(self.project_folder+'/Documentos_base'):
                        shutil.rmtree(self.project_folder+'/Documentos_base', True)
                    shutil.copytree(pfcdf,self.project_folder+'/Documentos_base', symlinks=False, ignore=None)
                        
                

    @api.multi
    def set_posible(self):
        pfc = self.project_filesystem_config or False
        if pfc != False:
            pfccf = self.cotizacion_folder
            pfcpf = self.project_folder
        #si viene de presupuestar, no se mueve nada.
        if self.state == 'arrancar': # viene de trabajos/abiertos (arrancar) hay que moverlo a cotizacion
            if self.project_folder_exist:
                shutil.move(pfcpf,pfccf)
                
        return super(project_project, self).set_posible(context=self._context)


    @api.multi
    def set_arrancar(self):
        pfc = self.project_filesystem_config or False
        if pfc != False:
            pfccf = self.cotizacion_folder
            pfcpf = self.project_folder
            
        
        result = ''
        if self.state == 'posible':  #viene de cotizacion (posible), lo movemos a proyecto/abierto
                if self.cotizacion_folder_exist:
                    shutil.move(pfccf,pfcpf)
        if self.state == 'terminar':  #viene de cotizacion (posible), lo movemos a proyecto/abierto
                result = super(project_project, self).set_arrancar(context=self._context) 
                if self.project_folder_exist:
                    #recalcular project_folder
                    self.compute_project_folder()
                    shutil.move(pfcpf,self.project_folder)
                        
        if result == '':
            result = super(project_project, self).set_arrancar(context=self._context)
        return result

    @api.multi
    def set_terminar(self):
        pfc = self.project_filesystem_config or False
        pfcpf = ''
        if pfc != False:
            pfcpf = self.project_folder
            
        result = ''
        #si viene de cobrar se queda donde esta, el proyecto no se mueve
        if self.state == 'arrancar':  #proyecto/abierto, lo movemos a terminados para cobrar
                result = super(project_project, self).set_terminar(context=self._context) 
                if os.path.exists(pfcpf):
                    #recalcular project_folder
                    self.compute_project_folder()
                    shutil.move(pfcpf, self.project_folder)
        if result == '':
            result = super(project_project, self).set_terminar(context=self._context)
        return result


    @api.multi
    def set_cobrar(self):
        pfc = self.project_filesystem_config or False
        pfcpf =''
        if pfc != False:
            pfcpf = self.project_folder
        result = ''
            
        if self.state == 'cerrado':
            result = super(project_project, self).set_cobrar(context=self._context)
            if os.path.exists(pfcpf):
                #recalcular project_folder
                self.compute_project_folder()
                #si viene de cerrado, lo movemos a terminados para cobrar.
                shutil.move(pfcpf, self.project_folder)
        if result == '':
            result = super(project_project, self).set_cobrar(context=self._context)
        return result

    @api.multi
    def set_cerrado(self):
            #hay que buscar el proyecto en cotizacion o trabajos
            #hay que mover el proyecto a cerrado
        pfc = self.project_filesystem_config or False
        if pfc != False:
            pfcpf = self.project_folder
            pfccf = self.cotizacion_folder
            result = super(project_project, self).set_cerrado(context=self._context)

            if os.path.exists(pfcpf) :
                self.compute_project_folder()
                shutil.move(pfcpf, self.project_folder)
            else:
                if os.path.exists(pfccf):
                    self.compute_cotizacion_folder()
                    shutil.move(pfccf, self.cotizacion_folder)
 
        if result == '':
            result = super(project_project, self).set_cerrado(context=self._context)

        return result

