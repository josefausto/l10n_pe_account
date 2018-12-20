# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from datetime import datetime

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    
    pe_affectation_code = fields.Selection(selection= "_get_pe_reason_code", string="Type of affectation", help="Type of affectation to the IGV")
    
    @api.model
    def _get_pe_reason_code(self):
        return self.env['pe.datas'].get_selection("PE.CPE.CATALOG7")
    
    
    