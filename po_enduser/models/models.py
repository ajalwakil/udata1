# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    

    customer_sale_id = fields.Many2one('res.partner', string='Customer Details')
    domain = fields.Char('Domain')
    subscription_status = fields.Selection([('new', 'New'), ('renew', 'Renew'), ('addon', 'Add-on')])
    period = fields.Selection([('monthly', 'Monthly'), ('yearly', 'Yearly')])
    approved_by_id = fields.Many2one('hr.employee', string='Approved By')
    referred_by = fields.Many2one('res.partner' , string = 'Referred')
    
    def action_rfq_send(self):
        res = super(PurchaseOrder, self).action_rfq_send()

        '''
        Overwrite Action Send
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            if self.env.context.get('send_rfq', False):
                template_id = ir_model_data._xmlid_lookup('purchase.email_template_edi_purchase')[1]
            else:
                template_id = ir_model_data._xmlid_lookup('purchase.email_template_edi_purchase_done')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data._xmlid_lookup('mail.email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict(self.env.context or {})
        ctx.update({
            'default_model': 'purchase.order',
            'default_res_ids': self.ids,
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'default_email_layout_xmlid': "mail.mail_notification_layout_with_responsible_signature",
            'force_email': True,
            'mark_rfq_as_sent': True,
        })

        
        lang = self.env.context.get('lang')
        if {'default_template_id', 'default_model', 'default_res_id'} <= ctx.keys():
            template = self.env['mail.template'].browse(ctx['default_template_id'])
            if template and template.lang:
                lang = template._render_lang([ctx['default_res_id']])[ctx['default_res_id']]

        self = self.with_context(lang=lang)
        if self.env.context.get('send_rfq', False):
            ctx['model_description'] = _('Request for Quotation')
        else:
            ctx['model_description'] = _('Purchase Order')

        return res

