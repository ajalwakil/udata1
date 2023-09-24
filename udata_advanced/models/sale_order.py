# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo import models, fields, api,_


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_terms_and_conditions = fields.Text(string='Terms and Conditions')
    arabic_sale_terms_and_conditions = fields.Text(string='Terms and Conditions')
    next_number = fields.Integer(default=1,copy=False)
    sale_reversion_id = fields.Many2one("sale.order")
    versioned = fields.Boolean(copy=False)
    sale_order_ids = fields.One2many(comodel_name="sale.order", inverse_name="sale_reversion_id",  string="Sales Orders", required=False, readonly=1)
    date_order = fields.Datetime(string='Order Date', required=True, readonly=False, index=True, copy=False,
                                 default=fields.Datetime.now,
                                 help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")
    date_order_check = fields.Boolean('date order check',compute='_compute_date_order_check')
    product_code = fields.Boolean(string='Print Product Code')
    all_price = fields.Boolean(string='Print Product Price')
    Customer_hide = fields.Boolean('Customer hide')
    Customer_name = fields.Char('Customer Name')
    Customer_company = fields.Char('Customer Company')
    Customer_phone = fields.Char('Customer Phone')
    Customer_email = fields.Char('Customer Email')


    def _compute_date_order_check(self):
        check_date_order = self.env['res.users'].has_group('udata_advanced.group_sale_date_order_access')
        self.date_order_check = False
        if check_date_order:
            self.date_order_check = True




    @api.model
    def default_get(self, fields):
        res = super(SaleOrder, self).default_get(fields)
        sale_terms_and_conditions = self.env["ir.config_parameter"].sudo().get_param(
            "udata_advanced.sale_terms_and_conditions", False)
        arabic_sale_terms_and_conditions = self.env["ir.config_parameter"].sudo().get_param(
            "udata_advanced.arabic_sale_terms_and_conditions", False)
        res.update({
            'sale_terms_and_conditions': sale_terms_and_conditions or False,
            'arabic_sale_terms_and_conditions': arabic_sale_terms_and_conditions or False,
                    })
        return res



    def _get_url_order(self):
        return 'https://udata.odoo.com' + self.get_portal_url()


    def action_reversion(self):
        if self.state not in ['draft', 'sent']:
            return
        history_order = self.copy()
        orders =  self.sale_order_ids.ids + [self.id]
        history_order.sale_order_ids = orders
        if orders:
            history_order.name = history_order.sale_order_ids.sorted(lambda o: o.create_date)[0].name + "-" + str(len(history_order.sale_order_ids))
        for order in history_order.sale_order_ids:
            order.versioned = True

        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'res_id': history_order.id,
            'type': 'ir.actions.act_window',
        }
        return history


    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self.sale_order_ids:
            if order.versioned == False:
                raise ValidationError(_("Order %s has been confirmed")%order.name)
        for order in self:
            order.sale_reversion_id.versioned = True
            order.versioned = False
        return res

    @api.onchange('partner_id')
    def _onchange_partner(self):
        self.Customer_hide = False
        if self.partner_id.name == 'General Cash Customer':
            self.Customer_hide = True
