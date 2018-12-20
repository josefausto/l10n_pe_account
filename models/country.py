# -*- coding: utf-8 -*-

from odoo import fields, models, api

class Country(models.Model):
    _inherit = 'res.country'
    
    pe_country_code = fields.Selection(selection="_get_country_code", string="Country Code")
    
    @api.model
    def _get_country_code(self):
        return self.env['pe.datas'].get_selection("PE.TABLA35")
    