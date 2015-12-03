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

from datetime import datetime, date
import time
from openerp import models, api
from openerp.osv import fields, osv
from openerp.tools.translate import _

class project_project(osv.osv):
    _inherit = 'project.project'

    def compute_name(self,  cr, uid, ids,name,args,context):
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            projectTypeCode = ''
            partnerName = ''
            companyName = ''
            if record.type_project_id:
                projectTypeCode = record.type_project_id.code or ''
            if record.partner_id:
                if record.partner_id.is_company:
                    companyName = record.partner_id.name or ''
                else:
                    partnerName = record.partner_id.name or ''
                    if record.partner_id.commercial_partner_id:
                        companyName = record.partner_id.commercial_partner_id.name or ''
            
            companyName = ('-'+str(companyName)) if companyName else ''
            partnerName = ('-'+str(partnerName)) if partnerName else ''
            result = str(date.today().year)  + '-' + str(record.id or '') + '-' + str(projectTypeCode) + '-PR-' + str(record.name) + companyName + partnerName  
            res.append((record.id, result))

        return res
    
    
    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
    
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            res.append((record.id, record.nombre_completo))
        
        return res
    
    
    _columns = {
        'nombre_completo': fields.function (compute_name, string="Nombre de Proyecto",type='char',help="ayuda"),
        'resource_calendar_id': fields.many2one('resource.calendar', 'Working Time', help="Timetable working hours to adjust the gantt diagram report", 
                                                states={'cerrado':[('readonly',True)]} ),
        'type_ids': fields.many2many('project.task.type', 'project_task_type_rel', 'project_id', 'type_id', 'Tasks Stages', states={'cerrado':[('readonly',True)]}),
        'user_ids': fields.many2many('res.users', 'project_user_type_rel', 'project_id', 'user_id', 'Project Managers', states={'cerrado':[('readonly',True)]}),
        'state': fields.selection([('presupuestar', 'Presupuestar'),
                                   ('posible','Posible'),
                                   ('arrancar','Arrancar'),
                                   ('terminar', 'Terminar'),
                                   ('cobrar','Cobrar'),
                                   ('cerrado','Cerrado')],
                                  'Status', required=True, copy=False),
        'type_project_id': fields.many2one('project.project.type'),        
        'start_date': fields.date(string="Fecha de Inicio")        
    }

    _defaults = {
        'active': True,
        'type': 'contract',
        'use_tasks': True,
        'label_tasks': 'Tareas',
        'state': 'presupuestar',
        'sequence': 10,
        'start_date': fields.datetime.now(),
        'user_id': lambda self,cr,uid,ctx: uid,
        'alias_model': 'project.task',
        'privacy_visibility': 'employees',
    }


    def set_template(self, cr, uid, ids, context=None):
        self.setActive(cr, uid, ids, value=False, context=context)
        #return self.write(cr, uid, ids, {'state': 'presupuestar'}, context=context)


    def addDefaultTask(self, selfparam, cr, uid, ids,estado='presupuestar'):
        ##crear nuevas task
        for record in self.browse(cr, uid, ids, None):
            typeTaskIds = self.pool.get('project.project.type.task').search(cr,uid,[('state_project','=',estado),('type','=',record.type_project_id['id'])])
        
            typeTask = self.pool.get('project.project.type.task')
            
            task_obj = self.pool['project.task']

            for taskTemplate in typeTask.browse(cr,uid,typeTaskIds).tasks:
                defaults = {'name': taskTemplate.name,'project_id':record.id}
                task_exist = task_obj.search(cr, uid, [('project_id','=', record.id),('name','=',taskTemplate.name)])
                if not task_exist:
                    targetTask =  task_obj.create(cr, uid, defaults, None)


    def set_presupuestar(self, cr, uid, ids, context=None):
        self.addDefaultTask(self, cr, uid, ids, 'presupuestar')
        return self.write(cr, uid, ids, {'state': 'presupuestar'}, context=context)

    def set_posible(self, cr, uid, ids, context=None):
        self.addDefaultTask(self, cr, uid, ids,'posible')
        return self.write(cr, uid, ids, {'state': 'posible'}, context=context)

    def set_arrancar(self, cr, uid, ids, context=None):
        self.addDefaultTask(self, cr, uid, ids,'arrancar')
        return self.write(cr, uid, ids, {'state': 'arrancar'}, context=context)

    def set_terminar(self, cr, uid, ids, context=None):
        self.addDefaultTask(self, cr, uid, ids,'terminar')
        return self.write(cr, uid, ids, {'state': 'terminar'}, context=context)

    def set_cobrar(self, cr, uid, ids, context=None):
        self.addDefaultTask(self, cr, uid, ids,'cobrar')
        return self.write(cr, uid, ids, {'state': 'cobrar'}, context=context)

    def set_cerrado(self, cr, uid, ids, context=None):
        self.addDefaultTask(self, cr, uid, ids,'cerrado')
        return self.write(cr, uid, ids, {'state': 'cerrado'}, context=context)

    def reset_project(self, cr, uid, ids, context=None):
        #remove all task?
        return self.setActive(cr, uid, ids, value=True, context=context)

    def duplicate_template(self, cr, uid, ids, context=None):
        context = dict(context or {})
        data_obj = self.pool.get('ir.model.data')
        result = []
        for proj in self.browse(cr, uid, ids, context=context):
            context.update({'analytic_project_copy': True})
            new_date_start = time.strftime('%Y-%m-%d')
            new_date_end = False
            if proj.date_start and proj.date:
                start_date = date(*time.strptime(proj.date_start,'%Y-%m-%d')[:3])
                end_date = date(*time.strptime(proj.date,'%Y-%m-%d')[:3])
                new_date_end = (datetime(*time.strptime(new_date_start,'%Y-%m-%d')[:3])+(end_date-start_date)).strftime('%Y-%m-%d')
            context.update({'copy':True})
            new_id = self.copy(cr, uid, proj.id, default = {
                                    'name':_("%s (copy)") % (proj.name),
                                    'state':'presupuestar',
                                    'date_start':new_date_start,
                                    'date':new_date_end}, context=context)
            result.append(new_id)

        if result and len(result):
            res_id = result[0]
            form_view_id = data_obj._get_id(cr, uid, 'project', 'edit_project')
            form_view = data_obj.read(cr, uid, form_view_id, ['res_id'])
            tree_view_id = data_obj._get_id(cr, uid, 'project', 'view_project')
            tree_view = data_obj.read(cr, uid, tree_view_id, ['res_id'])
            search_view_id = data_obj._get_id(cr, uid, 'project', 'view_project_project_filter')
            search_view = data_obj.read(cr, uid, search_view_id, ['res_id'])
            return {
                'name': _('Projects'),
                'view_type': 'form',
                'view_mode': 'form,tree',
                'res_model': 'project.project',
                'view_id': False,
                'res_id': res_id,
                'views': [(form_view['res_id'],'form'),(tree_view['res_id'],'tree')],
                'type': 'ir.actions.act_window',
                'search_view_id': search_view['res_id'],
            }

    # set active value for a project, its sub projects and its tasks
    def setActive(self, cr, uid, ids, value=True, context=None):
        task_obj = self.pool.get('project.task')
        for proj in self.browse(cr, uid, ids, context=None):
            self.write(cr, uid, [proj.id], {'state': value and 'presupuestar' or 'template'}, context)
            cr.execute('select id from project_task where project_id=%s', (proj.id,))
            tasks_id = [x[0] for x in cr.fetchall()]
            if tasks_id:
                task_obj.write(cr, uid, tasks_id, {'active': value}, context=context)
            child_ids = self.search(cr, uid, [('parent_id','=', proj.analytic_account_id.id)])
            if child_ids:
                self.setActive(cr, uid, child_ids, value, context=None)
        return True
    

class project_task(osv.osv):
    _inherit = ['project.task']

    def _is_template(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for task in self.browse(cr, uid, ids, context=context):
            res[task.id] = True
            if task.project_id:
                if task.project_id.active == False or task.project_id.state == 'presupuestar':
                    res[task.id] = False
        return res


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
