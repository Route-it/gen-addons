# -*- coding: utf-8 -*-

from openerp import models, fields, api

class fleet_expiration(models.Model):
    _name = 'fleet_expirations.fleet_expiration'

    name = fields.Char()
    