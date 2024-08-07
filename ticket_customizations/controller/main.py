# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo import models, _
from odoo.addons.website.controllers import form
from odoo.exceptions import UserError, ValidationError


class WebsiteForm(form.WebsiteForm):

    def _handle_website_form(self, model_name, **kwargs):
        email = request.params.get('partner_email')
        email_test = ''
        
           
        if email:
            user_id = request.env['res.users'].sudo().search([('email', '=', email)], limit=1)
            if not user_id:

                raise UserError(_(
                "\n" +                                          
                                "The ticket can not be submit due to unrecognized email           | \n \n"
                                 " \n \n  نأسف لعدم امكانية فتح تذكرة الدعم، لعدم وجود بريدك الالكتروني في سجلاتنا") )


            if request.env.user.email == email:
                partner = request.env.user.partner_id
                email_test = request.env.user.email
            else:
                partner = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
            if not partner:
                partner = request.env['res.partner'].sudo().create({
                    'email': email,
                    'name': request.params.get('partner_name', False)
                })
            request.params['partner_id'] = partner.id

           
        return super(WebsiteForm, self)._handle_website_form(model_name, **kwargs)
