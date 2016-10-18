# -*- coding: utf-8 -*-

import logging
from openerp import models, fields, api
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


_logger = logging.getLogger(__name__)

def _models_get(self):
    model_obj = self.env['ir.model'] 
    model_list = model_obj.search([('model', 'in', ('res.partner','fleet.vehicle','hr.employee','ir.attachment'))])
    #('model','=','res.users'),'|',('model','=','hr.employee'),
    
    return [(model.model, model.name) for model in model_list]

"""
class expirations_attendee(models.Model):
    _name = "expirations.attendee"
    _inherit = 'calendar.attendee'
    event_id = fields.Many2one('expirations.expirations', 'Expiration Linked', ondelete='cascade')
"""


class expirations(models.Model):
    #_name = 'expirations.expirations'
    #_inherits = {'calendar.event':'calendar_event_id'}
    _inherit = 'calendar.event'

    res_id = fields.Reference(
        selection=_models_get,
        string='Recurso'
    )

    name = fields.Char('Asunto')

    start_date = fields.Date('Fecha de vencimiento')
    #partner_ids = fields.Many2many(string="Responsables",column1='calendar_event_id')
    #partner_ids = fields.Many2many('res.partner', 'expirations_event_res_partner_rel',column1='calendar_event_id' , string='Responsables', states={'done': [('readonly', True)]})
    #categ_ids = fields.Many2many('calendar.event.type', 'meeting_category_rel', 'event_id', 'type_id', 'Tags')

    #attendee_ids = fields.One2many('expirations.attendee', inverse_name='event_id', string='Attendees', ondelete='cascade')
    #alarm_ids = fields.Many2many('calendar.alarm', 'calendar_alarm_calendar_event_rel',column1='calendar_event_id', string='Reminders', ondelete="restrict", copy=False)

    """
        args['comodel_name'] = self._obj
        args['relation'] = self._rel
        args['column1'] = self._id1
        args['column2'] = self._id2
        args['limit'] = self._limit
        'partner_ids': fields.many2many('res.partner', 'calendar_event_res_partner_rel', string='Attendees', states={'done': [('readonly', True)]}),
    """




    #start_date = fields.Date(related='calendar_event_id.start_date','Fecha de vencimiento')
    #start = fields.Date(related='calendar_event_id.start_date','Fecha de vencimiento')
    #stop = fields.Date(related='calendar_event_id.start_date','Fecha de vencimiento')
    #stop_date = fields.Date(related='calendar_event_id.start_date','Fecha de vencimiento')
    #calendar_event_id = fields.Many2one('calendar.event', required=True, ondelete='cascade')

    
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        
        
        if (bool(context.get('resources')) & (context.get('resources') == 'expirations') ):
            categ_ids_to_add = self.pool["calendar.event.type"].search(cr, uid, [('name', 'ilike', 'xpiration')], context=context)
            if (vals.has_key('categ_ids')):
                vals.update({'categ_ids':[[6,False,categ_ids_to_add]]})
                vals.update({'allday':True})
        
        res = super(expirations, self).create(cr, uid, vals, context=context)

        return res
    """
    #Sirve para modificar los valores por defecto de la vista
    @api.model
    def default_get(self, fields):
        context = self._context or {}
        res = super(expirations, self).default_get(fields)

        if (bool(context.get('view_id'))):
            res.update({'delivery_id': context.get('delivery_id')})
            #res.update({'categ_ids': a_default_expiration_categ})
        
        return res


    #Sirve para modificar la vista
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(expirations, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=False)
        context = self._context or {}
        if (res['name'] == 'Vencimiento') & (view_type == 'form'):
            for field in res['fields']:
                if field == 'allday':
                    #res['fields'][field] = True
                    res['fields'][field].update({'context': {'value':True}})
                    res['fields'][field].update({'change_default': True})
        return res
    """


    
    """
    _defaults = {
               'allday':True
    }
    """
     
    @api.onchange('start_date')
    def onchange_start_date(self):
        self.start = self.start_date
        self.stop = self.start_date
        self.stop_date = self.start_date
        self.allday = True
        self.onchange_dates('start', self.start_date, self.stop_date, self.allday, True)
        #self.calendar_event_id.onchange_dates('start', self.start_date, self.stop_date, self.allday, True)
     
    def onchange_duration(self, cr, uid, ids, start=False, duration=False, context=None):
        value = {}
        if not (start and duration):
            return value
        start = datetime.strptime(start, DEFAULT_SERVER_DATETIME_FORMAT)
        value['stop_date'] = (start + timedelta(hours=duration)).strftime(DEFAULT_SERVER_DATE_FORMAT)
        value['stop_datetime'] = (start + timedelta(hours=duration)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        value['start'] = start.strftime(DEFAULT_SERVER_DATE_FORMAT)
        value['stop'] = start.strftime(DEFAULT_SERVER_DATE_FORMAT)
        return {'value': value}
    
    
#    @api.onchange('partner_ids') 
#    def onchange_partners(self):
#        self.onchange_partner_ids(self.partner_ids)
#	  self.calendar_event_id.onchange_partner_ids(self.partner_ids)
        
            
    @api.multi
    def exec_advice(self):
        _logger.info('Advice excecuted' + (self.advice_method or 'empty') )
        True

#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100