# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    available_quantity = fields.Float('Available Quantity')

    @api.onchange('product_id')
    def _onchange_qty_available_product_id(self):
        self.available_quantity = self.product_id.qty_available