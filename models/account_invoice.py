# -*- coding: utf-8 -*-

from odoo import api, exceptions, fields, models, _

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def invoice_line_move_line_get(self):
        res = super(AccountInvoice, self).invoice_line_move_line_get()
        for i in range(len(res)):
            line_id = self.env['account.invoice.line'].browse(res[i]['invl_id'])
            res[i]['pe_affectation_code'] = line_id.pe_affectation_code
        return res