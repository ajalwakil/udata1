# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def product_id_change_custom(self):
        if self.product_id:
            self.name = self.product_id.name
        else:
            self.name = ''


