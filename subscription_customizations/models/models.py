# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class SaleSubscriptionInherit(models.Model):
    _inherit = 'sale.subscription'

    trigger_date = fields.Date(string='Trigger Date',readonly=False, tracking=True,compute='_compute_trigger_date')

    @api.depends('date')
    def _compute_trigger_date(self):
        self.trigger_date = False
        if self.date:
            self.trigger_date = self.date + relativedelta(months=-1)