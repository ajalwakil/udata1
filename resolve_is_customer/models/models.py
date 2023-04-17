# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    is_customer = fields.Boolean(string="Is Customer")
    is_vendor = fields.Boolean(string="Is Vendor")