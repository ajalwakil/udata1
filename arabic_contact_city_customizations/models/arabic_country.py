# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ArabicCountry(models.Model):
    _description = "Arabic Country"
    _name = 'res.country.arabic'

    name = fields.Char(string='Arabic Country Name')
