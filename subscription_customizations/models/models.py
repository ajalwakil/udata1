# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleSubscriptionInherit(models.Model):
    _inherit = 'sale.subscription'

    trigger_date = fields.Date(string='Trigger Date', tracking=True)