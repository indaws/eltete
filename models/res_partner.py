﻿
from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    
    special_conditions = fields.Text('Condiciones especiales')
    uploading_time = fields.Text('Horarios descarga')
    ice = fields.Char('ICE')
    

    num_bailen = fields.Integer('Num Bailén')
    
    prod_comment_ids = fields.One2many('partner.product.comments', 'partner_id', string="Observaciones productos")
    
    MOL = [('ML','MUELLE O LATERAL'),   
              ('SM','SOLO MUELLE'),
              ('SL','SOLO LATERAL'),
             ]
    carga = fields.Selection(selection=MOL, string='Carga', default='ML', )

    
    
    referencia_cliente_count = fields.Integer(compute='_compute_referencia_cliente_count', string='Referencia cliente Count')
    referencia_cliente_ids = fields.One2many('sale.referencia.cliente', 'partner_id', 'Referencias cliente')
    
    def _compute_referencia_cliente_count(self):
        self.referencia_cliente_count = len(self.env['sale.referencia.cliente'].search([('partner_id', '=', self.id),]))
    
    sale_oferta_count = fields.Integer(compute='_compute_sale_oferta_count', string='Sale Offer Count')
    sale_oferta_ids = fields.One2many('sale.offer.oferta', 'partner_id', 'Ofertas')
    
    def _compute_sale_oferta_count(self):
        self.sale_oferta_count = len(self.env['sale.offer.oferta'].search([('partner_id', '=', self.id),]))
        
    sale_cotizacion_count = fields.Integer(compute='_compute_sale_cotizacion_count', string='Sale Cotización Count')
    sale_cotizacion_ids = fields.One2many('sale.cotizacion', 'partner_id', 'Cotizaciones')
    
    def _compute_sale_cotizacion_count(self):
        self.sale_cotizacion_count = len(self.env['sale.cotizacion'].search([('partner_id', '=', self.id),]))
        
    
    
class partner_product_comments(models.Model):
    _name = 'partner.product.comments'

    partner_id = fields.Many2one('res.partner', string="Cliente")
    product_id = fields.Many2one('product.template', string="Producto")
    comments = fields.Text('Comentarios')
    
    