# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CrmLeadInherit(models.Model):
    _inherit = 'crm.lead'

    # def action_new_quotation(self):
    #     action = self.env["ir.actions.actions"]._for_xml_id("sale_crm.sale_action_quotations_new")
    #     # custom_field_value = self.contact_name if hasattr(self, 'contact_name') else False
    #     action['context'] = {
    #         'search_default_opportunity_id': self.id,
    #         'default_opportunity_id': self.id,
    #         'search_default_partner_id': self.partner_id.id,
    #         'default_partner_id': self.partner_id.id,
    #         'default_campaign_id': self.campaign_id.id,
    #         'default_medium_id': self.medium_id.id,
    #         'default_origin': self.name,
    #         'default_source_id': self.source_id.id,
    #         'default_company_id': self.company_id.id or self.env.company.id,
    #         'default_tag_ids': [(6, 0, self.tag_ids.ids)],
    #         'default_Customer_name': self.contact_name,
    #     }
    #     if self.team_id:
    #         action['context']['default_team_id'] = self.team_id.id,
    #     if self.user_id:
    #         action['context']['default_user_id'] = self.user_id.id
    #     return action



    def action_new_quotation(self):
        action = super(CrmLeadInherit, self).action_new_quotation()
        # Make the lead's Assigned Partner the quotation's Referrer.
        action['context']['default_Customer_name'] = self.contact_name
        action['context']['default_Customer_company'] = self.partner_name
        action['context']['default_Customer_phone'] = self.mobile
        action['context']['default_Customer_email'] = self.email_from
        return action
