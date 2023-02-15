# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ArabicCountryCity(models.Model):
    _description = "Arabic City"
    _name = 'res.city.arabic'

    name = fields.Char(string='Arabic City Name')