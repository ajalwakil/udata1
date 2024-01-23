# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SetCompanyForProducts(models.Model):
    _inherit = 'product.product'

    def set_company_product(self):
        # Replace 'your_company_id' with the actual ID of the company you want to set.
        company_id = self.env['res.company'].search([('name', '=', "UDATA Co.")], limit=1)

        if company_id:
            product_idz = self.env['product.product'].search([])
            product_idz.write({'company_id': company_id.id})
            product_idz.update({'company_id': company_id.id})
