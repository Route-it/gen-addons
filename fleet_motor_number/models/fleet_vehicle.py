# -*- coding: utf-8 -*-

from openerp import models, fields

class fleet_vehicle(models.Model):
    _inherit = 'fleet.vehicle'

    motor_number = fields.Char(string="Numero de Motor")

