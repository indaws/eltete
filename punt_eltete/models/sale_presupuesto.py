
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

    
class sale_presupuesto(models.Model):
    _name = 'sale.presupuesto'

    name = fields.Char(string='Nueva oferta', required=True, copy=False, readonly=True, index=True, default=lambda self: "/")
    
    
    partner_id = fields.Many2one('res.partner', string="Cliente", required=True)
    user_id = fields.Many2one('res.users', string="Comercial", default=lambda self: self.env.user, required=True)
    date = fields.Date('Fecha', default=fields.Date.today(), required=True)
    
    
    
    
    
    
class sale_presupuesto_line(models.Model):
    _name = 'sale.presupuesto.line'
    
    presupuesto_id = fields.Many2one('sale.presupuesto', string="Presupuesto", required=True)
    user_id = fields.Many2one('res.users', string="Comercial", default=lambda self: self.env.user, required=True)
    date = fields.Date('Fecha', default=fields.Date.today(), required=True)
    npallets = fields.Integer('Num pallets')
    emetro = fields.Float('Emetro')
    eton = fields.Float('Eton')
    #etipo = fields.Integer('Etipo')
    state_id = fields.Many2one('res.country.state', string="Provincia")
    country_id = fields.Many2one('res.country', string="País")
    activa = fields.Boolean("Activa")
    enviada = fields.Boolean("Enviada")
    usada = fields.Boolean("Usada")
    
    
    
    
    
    
    
    
    
    
    