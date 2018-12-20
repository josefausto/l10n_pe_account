# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class PeAccountAbstractReport(models.AbstractModel):
    _name = "pe.account.abstract.report"
    
    name = fields.Char("Name", copy = False, default='/')
    company_id = fields.Many2one('res.company', string='Company', change_default=True,
        required=True, readonly=True, states={'draft': [('readonly', False)]},
        default=lambda self: self.env['res.company']._company_default_get('pe.account.abstract.report'))
    date = fields.Date("Date", default = fields.Date.context_today, required = True, readonly=True, states={'draft': [('readonly', False)]})
    start_date = fields.Date("Start Date", required = True, readonly=True, states={'draft': [('readonly', False)]})
    end_date = fields.Date("End Date", required = True, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'), 
                              ('generated', 'Generated'), ('done', 'Done'), 
                              ('cancelled', 'Cancelled')], readonly=True, default='draft', copy=False, string="Status")
    attachment_id = fields.Many2one('ir.attachment', "Data", readonly=True, states={'draft': [('readonly', False)]})
    datas_fname = fields.Char('File Name', compute='_compute_datas', inverse='_inverse_datas', readonly=True, states={'draft': [('readonly', False)]})
    datas = fields.Binary(string='File Content', compute='_compute_datas', inverse='_inverse_datas', readonly=True, states={'draft': [('readonly', False)]})
    type = fields.Selection([], required = True, readonly=True, states={'draft': [('readonly', False)]})
    
    presentation_code = fields.Selection(selection= "_get_presentation_code", string="Presentation", 
                                         help="Código de oportunidad de presentación del EEFF, aplica al Libro de Inventarios y Balances, para los demás consigne '00'")
    operation_code = fields.Selection(selection="_get_operation_code", string="Operation", help="Indicador de operaciones")
    indicator_code = fields.Selection(selection="_get_indicator_code", string="Content", help="Indicador del contenido del libro o registro", default="1")
    currency_code = fields.Selection(selection="_get_currency_code", string="Currency", help="Indicador de la moneda utilizada", default="1")
        
    @api.multi
    def get_le_name(self):
        self.ensure_one()
        le = self
        if le.type:
            vals = {}
            vals['ruc'] = le.company_id.partner_id.doc_number or ""
            if le.start_date and le.type:
                if le.type[0:2] in ['03', '12', '13']:
                    vals['periodo'] = datetime.strptime(le.start_date, "%Y-%m-%d").strftime('%Y%m%d')
                else:
                    vals['periodo'] = datetime.strptime(le.start_date, "%Y-%m-%d").strftime('%Y%m00')
            else:
                vals['periodo'] = ""
            
            vals['tipo'] = le.type or ""
            vals['presentacion'] = le.presentation_code or ""
            vals['operacion'] = le.operation_code or ""
            vals['indicador'] = le.indicator_code or ""
            vals['moneda'] = le.currency_code or ""
            name = "LE{ruc}{periodo}{tipo}{presentacion}{operacion}{indicador}{moneda}1".format(**vals)
            return name
        else:
            return ""
    
    @api.model
    def _get_presentation_code(self):
        return self.env['pe.datas'].get_selection("PE.LE.PRESENTACION")
    
    @api.model
    def _get_operation_code(self):
        return self.env['pe.datas'].get_selection("PE.LE.OPERACIONES")
    
    @api.model
    def _get_indicator_code(self):
        return self.env['pe.datas'].get_selection("PE.LE.INDICADOR")
    
    @api.model
    def _get_currency_code(self):
        return self.env['pe.datas'].get_selection("PE.LE.MONEDA")
    
    
    @api.multi
    @api.depends('attachment_id')
    def _compute_datas(self):
        for attach in self:
            if attach.attachment_id:
                attach.datas = attach.attachment_id.datas
                attach.datas_fname = attach.attachment_id.datas_fname

    @api.multi
    def _inverse_datas(self):
        for attach in self:
            if attach.datas_fname:
                vals = {
                    'name' : attach.datas_fname,
                    'datas' : attach.datas or b'',
                    'datas_fname' : attach.datas_fname,
                    'type' : 'binary'
                }
                if self.attachment_id:
                    self.attachment_id.write(vals)
                else:
                    attachment_id = self.env['ir.attachment'].create(vals)
                    self.attachment_id = attachment_id
    @api.one
    def action_draft(self):
        self.state = 'draft'
    
    @api.one
    def action_generated(self):
        self.state = 'generated'
    
    @api.one
    def action_done(self):
        self.state = 'done'
    
    @api.one
    def action_cancelled(self):
        self.state = 'cancelled'
    
    @api.multi
    def get_config(self):
        self.ensure_one()
        config_id = self.env["pe.account.config"].search([('company_id','=', self.company_id.id),('type','=', self.type)])
        if not config_id:
            raise UserError(_("There is no configuration"))
        return config_id
    