# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountPaymentInherit(models.Model):
    _inherit = "account.payment"

    bank_charges = fields.Monetary(currency_field='currency_id')
    vat_bank_charges = fields.Monetary(currency_field='currency_id', compute='_compute_vat_bank_charges')
    total_vat_bank_charges = fields.Monetary(currency_field='currency_id', compute='_compute_vat_bank_charges')

    @api.depends('bank_charges')
    def _compute_vat_bank_charges(self):
        self.vat_bank_charges = False
        self.total_vat_bank_charges = False
        for rec in self:
            if rec.bank_charges:
                rec.vat_bank_charges = (rec.bank_charges * 15) / 100
                rec.total_vat_bank_charges = rec.bank_charges + rec.vat_bank_charges

    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        # "function super for adding lines of bank charge payments"
        res = super(AccountPaymentInherit, self)._prepare_move_line_default_vals(write_off_line_vals=write_off_line_vals)
        self.ensure_one()
        write_off_line_vals = write_off_line_vals or {}

        write_off_amount_currency = write_off_line_vals.get('amount', 0.0)

        if self.payment_type == 'inbound':
            # Receive money.
            liquidity_amount_currency = self.amount
        elif self.payment_type == 'outbound':
            # Send money.
            liquidity_amount_currency = -self.amount
            write_off_amount_currency *= -1
        else:
            liquidity_amount_currency = write_off_amount_currency = 0.0

        payment_display_name = self._prepare_payment_display_name()

        default_line_name = self.env['account.move.line']._get_default_line_name(
            _("Internal Transfer") if self.is_internal_transfer else payment_display_name[
                '%s-%s' % (self.payment_type, self.partner_type)],
            self.total_vat_bank_charges,
            self.currency_id,
            self.date,
            partner=self.partner_id,
        )

        currency_id = self.currency_id.id
        debit = {
            'name': default_line_name,
            'date_maturity': self.date,
            'amount_currency': liquidity_amount_currency,
            'currency_id': currency_id,
            'debit': self.total_vat_bank_charges,
            'credit': 0,
            'partner_id': self.partner_id.id,
            # 'account_id':  self.outstanding_account_id.id,
            'account_id': self.journal_id.bank_charge_account.id,
        },
        credit = {
            'name': default_line_name,
            'date_maturity': self.date,
            'amount_currency': liquidity_amount_currency,
            'currency_id': currency_id,
            'debit': 0,
            'credit': self.total_vat_bank_charges,
            'partner_id': self.partner_id.id,
            # 'account_id': self.destination_account_id.id,
            'account_id': self.journal_id.default_account_id.id,

        },
        if self.total_vat_bank_charges:
            charge_list = []
            charge_list.extend(debit)
            charge_list.extend(credit)
            charge_list.extend(res)
            res = charge_list
        return res


class AccountJournalInherit(models.Model):
    _inherit = "account.journal"

    bank_charge_account = fields.Many2one('account.account')
