# -*- coding: utf-8 -*-

from openerp import models, fields, api

class fleet_vehicle_expiration(models.Model):
    _name = 'fleet.vehicle.expiration'

    name = fields.Char()
    due_date = fields.Date()
    fleet_vehicle = fields.Many2one("fleet.vehicle")
    