from odoo import models, fields, api


class SetCompanyForContacts(models.Model):
    _inherit = 'res.partner'

    def set_company(self):
        # Replace 'your_company_id' with the actual ID of the company you want to set.
        company_id = self.env['res.company'].search([('name', '=', "UDATA Co.")], limit=1)

        if company_id:
            contact_ids = self.env['res.partner'].search([])
            contact_ids.write({'company_id': company_id.id})
            contact_ids.update({'company_id': company_id.id})


# SetCompanyForContacts()