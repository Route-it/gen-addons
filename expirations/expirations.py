# -*- coding: utf-8 -*-

import logging
from openerp import models, fields, api

_logger = logging.getLogger(__name__)

class expirations(models.Model):
    _name = 'expirations.expirations'

    name = fields.Char()
    description = fields.Text()
    due_date = fields.Date()

    advices = fields.Many2many('expirations.advice')
     
class advice(models.Model):
    _name = 'expirations.advice'
     
    quantity = fields.Integer()
    unit = fields.Selection([('mins', 'minutes'),
                                   ('hours','hours'),
                                   ('days','days'),
                                   ('mons', 'mons')],
                                  'Unidad', required=True, copy=False)
     
    advice_method = fields.Text()
     
    @api.multi
    def exec_advice(self):
        _logger.info('Advice excecuted' + self.advice_method )
        True

#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100