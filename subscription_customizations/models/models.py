# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class SaleSubscriptionInherit(models.Model):
    _inherit = 'sale.subscription'

    trigger_date = fields.Date(string='Trigger Date Before 30 Days', store=True, tracking=True,compute='_compute_trigger_date')
    trigger_date_15 = fields.Date(string='Trigger Before 15 Days', store=True, tracking=True,compute='_compute_trigger_date')
    trigger_date_3 = fields.Date(string='Trigger Before 3 Days', store=True,tracking=True,compute='_compute_trigger_date')

    @api.depends('date')
    def _compute_trigger_date(self):
        self.trigger_date = False
        self.trigger_date_15 = False
        self.trigger_date_3 = False
        for rec in self:
            if rec.date:
                rec.trigger_date = rec.date + relativedelta(months=-1)
            if rec.date:
                rec.trigger_date_15 = rec.date + relativedelta(days=-15)
            if rec.date:
                rec.trigger_date_3 = rec.date + relativedelta(days=-3)



    def send_payment_reminder_email(self):
        # Calculate the current date
        today = fields.Date.today()

        # Your subscription is created
        subscriptions_created = self.env['sale.subscription'].search([
            ('date_start', '=', today), ('stage_id.category', '=', 'progress')
        ])
        if subscriptions_created:
            for subscription_c in subscriptions_created:
                template_c = self.env.ref('subscription_customizations.email_subscription_created')
                if template_c:
                    template_c.send_mail(subscription_c.id, force_send=True)

        # Send a payment reminder email to the subscriber before 30 days
        subscriptions_30_days = self.env['sale.subscription'].search([
            ('trigger_date', '=', today), ('stage_id.category', '=', 'progress')
        ])
        if subscriptions_30_days:
            for subscription_30 in subscriptions_30_days:
                template_30 = self.env.ref('subscription_customizations.email_payment_reminder_before_one_month')
                if template_30:
                    template_30.send_mail(subscription_30.id, force_send=True)

        # Send a payment reminder email to the subscriber before 15 days
        subscriptions_15_days = self.env['sale.subscription'].search([
            ('trigger_date_15', '=', today),
            ('stage_id.category', '=', 'progress')
        ])
        if subscriptions_15_days:
            for subscription_15 in subscriptions_15_days:
                template_15 = self.env.ref('subscription_customizations.email_payment_reminder_before_15_days')
                if template_15:
                    template_15.send_mail(subscription_15.id, force_send=True)

        # Send a payment reminder email to the subscriber before 3 days
        subscriptions_3_days = self.env['sale.subscription'].search([
            ('trigger_date_3', '=', today),
            ('stage_id.category', '=', 'progress')
        ])
        if subscriptions_3_days:
            for subscription_3 in subscriptions_3_days:
                template_3 = self.env.ref('subscription_customizations.email_payment_reminder_before_3_days')
                if template_3:
                    template_3.send_mail(subscription_3.id, force_send=True)

        # Subscription is expired
        expired_subscriptions = self.env['sale.subscription'].search(
            [('date', '=', today), ('stage_id.category', '=', 'progress')])
        if expired_subscriptions:
            for subscription_exp in expired_subscriptions:
                template_exp = self.env.ref('subscription_customizations.email_payment_expired')
                if template_exp:
                    template_exp.send_mail(subscription_exp.id, force_send=True)

        # Subscription is closed
        expired_closed = self.env['sale.subscription'].search(
            [('date', '=', today), ('stage_id.category', '=', 'closed')])
        if expired_closed:
            for subscription_cl in expired_closed:
                template_exp = self.env.ref('subscription_customizations.your_subscription_is_closed')
                if template_exp:
                    template_exp.send_mail(subscription_cl.id, force_send=True)


