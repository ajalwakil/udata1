# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseEndconsumer(models.Model):
    _inherit = "purchase.order"

    customer_sale_id = fields.Many2one('res.partner', string='Customer Details')
    domain = fields.Char('Domain')
    subscription_status = fields.Selection([('new', 'New'), ('renew', 'Renew'), ('addon', 'Add-on')])
    period = fields.Selection([('monthly', 'Monthly'), ('yearly', 'Yearly')])
    approved_by_id = fields.Many2one('hr.employee', string='Approved By')
