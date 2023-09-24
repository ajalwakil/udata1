# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLink(models.Model):
    _inherit = 'sale.order'

    share_link_field = fields.Char(string="Link", compute='_compute_share_link')

    @api.depends('name')
    def _compute_share_link(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for order in self:
            share_link = f"{base_url}/mail/view?model=sale.order&res_id={order.id}&access_token={order.access_token}"
            order.share_link_field = share_link