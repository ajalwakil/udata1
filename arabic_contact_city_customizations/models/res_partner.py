# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartnerArabic(models.Model):
    _inherit = 'res.partner'

    arabic_city_id_new = fields.Many2one("res.city.arabic", string='Arabic City')
    arabic_country_id_new = fields.Many2one('res.country.arabic', string='Arabic Country')


    @api.onchange('arabic_city_id_new')
    def _onchange_arabic_city_id_new(self):
        if self.arabic_city_id_new:
            self.arabic_city = self.arabic_city_id_new.name
            
    @api.onchange('arabic_country_id_new')
    def _onchange_arabic_country_id_new(self):
        if self.arabic_country_id_new:
            self.arabic_country_id = self.arabic_country_id_new.name
