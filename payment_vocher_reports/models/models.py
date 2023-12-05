# -*- coding: utf-8 -*-

from odoo import models, fields, api
from num2words import num2words


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    # cash_cheq_type = fields.Selection([
    #     ('cash', 'Cash'),
    #     ('cheq', 'Cheque'),
    #     ('transfer', 'Transfer')], string='Cash/Cheque/Transfer')

    cash_cheq_type = fields.Selection([
        ('cash', 'Cash'),
        ('cheq', 'Cheque')], string='Cash/Cheque')
    user_id_x = fields.Many2one('res.users',string='User', default=lambda self: self.env.user)
    bank_name = fields.Char('Bank Name')
    cheq_no = fields.Char('Cheq No')

    def amount_to_text(self, credit, currency):
        convert_amount_in_words = currency.amount_to_text(credit)
        # convert_amount_in_words = convert_amount_in_words.replace(' Rupees', ' Only ')
        return convert_amount_in_words

    # def amount_word(self, amount):
    #     language = self.partner_id.lang or 'en'
    #     language_id = self.env['res.lang'].search([('code', '=', 'ar_001')])
    #     if language_id:
    #         language = language_id.iso_code
    #     amount_str = str('{:2f}'.format(amount))
    #     amount_str_splt = amount_str.split('.')
    #     before_point_value = amount_str_splt[0]
    #     after_point_value = amount_str_splt[1][:2]
    #     before_amount_words = num2words(int(before_point_value), lang=language)
    #     after_amount_words = num2words(int(after_point_value), lang=language)
    #     amount = before_amount_words + ' ' + after_amount_words
    #     return amount
    
    def amount_word(self, amount):
        language = self.partner_id.lang or 'ar'
        language_id = self.env['res.lang'].search([('code', '=', 'ar_001')])
        if language_id:
            language = language_id.iso_code
        amount_str = str('{:2f}'.format(amount))
        amount_str_splt = amount_str.split('.')
        before_point_value = amount_str_splt[0]
        after_point_value = amount_str_splt[1][:2]
        before_amount_words = num2words(int(before_point_value), lang=language)
        after_amount_words = num2words(int(after_point_value), lang=language)
        if after_amount_words == 'صفر':
            amount = before_amount_words + ' ريال '
        else:
            amount = before_amount_words + ' ريال ' + ' و ' + after_amount_words + ' هللة '
        return amount
