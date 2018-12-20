# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PeAccountConfig(models.Model):
    _name = 'pe.account.config'

    name = fields.Char("Name", required = True)
    type = fields.Selection([], "Type", required = True)
    account_ids = fields.Many2many('account.account', string='Accounts')
    journal_ids = fields.Many2many("account.journal", string= "Journals")
    tax_ids = fields.Many2many('account.tax', string="Taxes")
    company_id = fields.Many2one('res.company', string='Company', change_default=True,
        required=True, default=lambda self: self.env['res.company']._company_default_get('pe.account.config'))
    igv_account_ids = fields.Many2many('account.account', string='IGV Tax Accounts', compute = "_get_account_ids")
    isc_account_ids = fields.Many2many('account.account', string='ISC Tax Accounts', compute = "_get_account_ids")
    other_account_ids = fields.Many2many('account.account', string='Other Tax Accounts', compute = "_get_account_ids")
    default_account_ids = fields.Many2many('account.account', string='Default Accounts', compute = "_get_account_ids")
    
    @api.multi
    @api.depends("tax_ids")
    def _get_account_ids(self):
        for config in self:
            config.igv_account_ids = config.tax_ids.filtered(lambda tax: tax.pe_tax_type.code == "1000").mapped('account_id').ids
            config.isc_account_ids = config.tax_ids.filtered(lambda tax: tax.pe_tax_type.code == "2000").mapped('account_id').ids
            config.other_account_ids = config.tax_ids.filtered(lambda tax: tax.pe_tax_type.code == "9999").mapped('account_id').ids
            default_account_ids = config.account_ids.ids +config.journal_ids.mapped('default_debit_account_id').ids+config.other_account_ids.ids
            config.default_account_ids = list(dict.fromkeys(default_account_ids).keys())
    
    @api.constrains("type")
    def check_doc_number(self):
        for config in self:
            if self.search_count([('company_id','=', config.company_id.id),
                                  ('type', '=', config.type)])>1:
                raise ValidationError(_('Config type already exists and violates unique field constrain'))

class PeAccountConfigLine(models.Model):
    _name = 'pe.account.config.line'
    
    name = fields.Char("Name", required=True)
    type = fields.Selection([('char', 'Char'),
                             ('integer', 'Integer'),
                             ('float', 'Float'),
                             ('date', 'Date'),
                             ('datetime', 'Date Time'),
                             ('sequence', 'Sequence')], 'Type', required=True, default='char')
    value = fields.Char("Value")
    format = fields.Char("Format")
    default = fields.Char("Default")
    