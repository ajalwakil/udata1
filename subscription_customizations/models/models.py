# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from datetime import datetime, timedelta

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

    def send_payment_reminder_email(self):
        # Calculate the current date
        today = fields.Date.today()

        # Find subscriptions with an expired subscription date
        expired_subscriptions = self.search([('date', '=', today),('stage_id.category', '=', 'progress')])
        if expired_subscriptions:
            for subscription in expired_subscriptions:
                # Send a payment reminder email to the subscriber
                template = self.env.ref('subscription_customizations.email_payment_expired')
                if template:
                    template.send_mail(subscription.id, force_send=True)