# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class SaleSubscriptionInherit(models.Model):
    _inherit = 'sale.subscription'

    trigger_date = fields.Date(string='Trigger Date Before 30 Days', tracking=True,compute='_compute_trigger_date')
    trigger_date_15 = fields.Date(string='Trigger Before 15 Days', tracking=True,compute='_compute_trigger_date')
    trigger_date_3 = fields.Date(string='Trigger Before 3 Days', tracking=True,compute='_compute_trigger_date')

    @api.depends('date')
    def _compute_trigger_date(self):
        self.trigger_date = False
        if self.date:
            self.trigger_date = self.date + relativedelta(months=-1)
        self.trigger_date_15 = False
        if self.date:
            self.trigger_date_15 = self.date + relativedelta(days=-15)
        self.trigger_date_3 = False
        if self.date:
            self.trigger_date_3 = self.date + relativedelta(days=-3)