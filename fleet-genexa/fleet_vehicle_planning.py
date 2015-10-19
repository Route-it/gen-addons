# -*- coding: utf-8 -*-

from datetime import datetime, date, timedelta
import time

from openerp import models, api
from openerp.osv import fields, osv
from openerp.tools.translate import _

from openerp.exceptions import ValidationError

class fleet_vehicle_planning(osv.osv):
    _name = "fleet.vehicle.planning"
    _description = "Planificacion de vehiculos"

    def _calendar_duration(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            # retorna la cantidad de horas totales - 1 porque el calendario toma hasta la hora 23.
            res[record.id] = (record.duration_days * 24) - 1
        return res

    _columns = {
                'fleet_vehicle_id': fields.many2one('fleet.vehicle', 'Vehiculo', help='ayuda',ondelete="set null",required=True),
                'date_start': fields.date('Fecha Inicio', select=True, copy=False,required=True),
                'duration_days':fields.integer('Duracion en dias',help="ayuda",required=True),
                'all_day':fields.boolean('Todo el dia',help="ayuda",default=True),
                'duration_days_calendar': fields.function (_calendar_duration,type='integer', string="Duracion",help="ayuda")

                #'date_end': fields.datetime('Fecha Fin', select=True, copy=False),
                #'duration_kanban':fields.function (_calcular_duracion_gantt,type='Integer'),
                #'descripcion':fields.Text('Descripcion adicional')

                ##
        #'task_ids': fields.one2many('project.task', 'project_id',
        #                            domain=[('stage_id.fold', '=', False)]),
        #'task_count': fields.function(_task_count, type='integer', string="Tasks",),
                
                #'sequence': fields.integer('Sequence', help="Gives the sequence order when displaying a list of Projects."),
                #'fleet_id': fields.many2one(
                #'fleet.vehicle', 'Vehiculo',
                # help="Texto de ayuda."
                # "otro renglon de dayuda.",
                # ondelete="cascade", required=True, auto_join=True),
    
    }
    
    
    # chequeo esto:
    # !(v1.start < vn.start < v1.end)
    # !(v1.start < vn.end < v1.end)
    
    
    @api.constrains('date_start','duration_days')
    def _check_date_start(self):
        for record in self:
            # filtro las planificaciones. Todas las que sean de el vehiculo en cuestion.
            # TODO: filtrar por fechas...
            vehicles = self.search([('fleet_vehicle_id', '=', record.fleet_vehicle_id['id']),
                                     ('id', '!=', record.id)])
            
            for vehicle in vehicles:
                # Armo las 2 fechas de fin para cada vehiculo a comparar
                vdate_start = datetime.strptime(vehicle.date_start, "%Y-%m-%d")
                rdate_start = datetime.strptime(record.date_start, "%Y-%m-%d")
                vehicle_end_date =  vdate_start + timedelta(days=vehicle.duration_days-1)
                record_end_date = rdate_start + timedelta(days=record.duration_days-1)
                # chequeo esto:
                # !(v1.start < v2.start < v1.end)
                # !(v1.start < v2.end < v1.end)
                if (
                    ( vdate_start <= rdate_start <= vehicle_end_date) 
                    or (vdate_start <= record_end_date <= vehicle_end_date) 
                    ):
                    raise ValidationError("La asignacion cae dentro del periodo de otra asignacion para ese vehiculo." % vehicle)
    # all records passed the test, don't return anything
    


   # def _calcular_duracion_gantt(self):
   #     return 24
    

    _sql_constraints = [
       ('duration_days_check','CHECK(duration_days > 0)','La duracion debe ser mayor que 0')
    ]

    


    #_constraints = [
        #(_check_dates, 'Error ! Task end-date must be greater than task start-date', ['date_start','date_end'])
        #(date_start == None,'La fecha es obligatoria'),
        #(_check_duration_days,'La duracion debe ser mayor que 0')
        
    #]


