# -*- coding: utf-8 -*-

import logging
from openerp import models, fields, api


_logger = logging.getLogger(__name__)

def _models_get(self):
    model_obj = self.env['ir.model'] 
    model_list = model_obj.search([('model', 'in', ('res.partner','fleet.vehicle','hr.employee','ir.attachment'))])
    #('model','=','res.users'),'|',('model','=','hr.employee'),
    
    return [(model.model, model.name) for model in model_list]

class expirations(models.Model):
    _inherit = 'calendar.event'

    res_id = fields.Reference(
        selection=_models_get,
        string='Recurso'
    )

    name = fields.Char('Asunto')

    start_date = fields.Date('Fecha de vencimiento')

    
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
     
    @api.onchange('start_date')
    def onchange_start_date(self):
        self.start = self.start_date
        self.stop = self.start_date
        self.stop_date = self.start_date
        self.allday = True
        self.onchange_dates('start', self.start_date, self.stop_date, self.allday, True)
     
        
            
    @api.multi
    def exec_advice(self):
        _logger.info('Advice excecuted' + (self.advice_method or 'empty') )
        True

