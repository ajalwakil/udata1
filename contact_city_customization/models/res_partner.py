# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    city_id = fields.Many2one("res.city", string='City')
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict',default=lambda self: self.env.company.country_id)

    @api.onchange('city_id')
    def _onchange_city_id(self):
        if self.city_id:
            self.city = self.city_id.name
