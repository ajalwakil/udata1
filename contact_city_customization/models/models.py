# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CountryCity(models.Model):
    _description = "Country City"
    _name = 'res.city'

    name = fields.Char(string='City Name')
