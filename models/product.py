from odoo import api, fields, models, _

class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _convert_prepared_anglosaxon_line(self, line, partner):
        res = super(ProductProduct, self)._convert_prepared_anglosaxon_line(line, partner)
        res['pe_affectation_code']=line.get('pe_affectation_code', False)
        return res