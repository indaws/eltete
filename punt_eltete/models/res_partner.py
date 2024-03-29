﻿
from odoo import fields, models, api

AGRUPADO = [('0','Sin Tipo'),
            ('1','Especial 660'),
            ('2','Camion Completo 700'),
            ('3','Agricultura 740'),
            ('4','Medio Camion 740'),
            ('11','Distribuidor Grande 780'),
            ('12','Distribuidor Mediano 820'),
            ('13','Distribuidor Pequeño 860'),
            ('14','Cliente Final Grande 820'), 
            ('15','Cliente Final Mediano 900'), 
            ('16','Cliente Final Pequeño 980'),
           ]

class ResPartner(models.Model):
    _inherit = 'res.partner'

    
    special_conditions = fields.Text('Condiciones especiales')
    uploading_time = fields.Text('Horarios descarga')
    ice = fields.Char('ICE')
    num_bailen = fields.Integer('Num Bailén')
    representante_legal = fields.Html('Representante Legal')
    eton_cantonera = fields.Integer('Cantonera €/t')
    eton_slipsheet = fields.Integer('SlipSheet €/t')
    
    #grupo_cliente = fields.Selection(selection=AGRUPADO,string = 'Clase Cliente',default = '0')
    
    
    prod_comment_ids = fields.One2many('partner.product.comments', 'partner_id', string="Observaciones productos")
    
    #entrega_principal_id = fields.Many2one('res.partner', 'partner_id', string="Entrega Principal")
    
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
        
    importe_pedido = fields.Float('Pedido sin facturar', digits = (12, 2), compute='_get_riesgo')
    importe_factura = fields.Float('Facturado sin Pagar', digits = (12, 2), compute='_get_riesgo')
    importe_riesgo = fields.Float('Riesgo Disponible', digits = (12, 2), compute='_get_riesgo')
    
    @api.depends('sale_order_ids')
    def _get_riesgo(self):
        for record in self:
            importe_pedido = 0.0
            importe_factura = 0.0
            
            for pedido in record.sale_order_ids:
                if pedido.estado != '4':
                    importe_pedido = importe_pedido + pedido.amount_total
            
            for factura in record.invoice_ids:
                factura_total = factura.amount_total_signed
                factura_no_pagado = factura.residual_signed
                importe_factura = importe_factura + factura_no_pagado
            
            importe_total = importe_pedido + importe_factura
            importe_riesgo = record.credit_limit - importe_total
            
            record.importe_pedido = importe_pedido
            record.importe_factura = importe_factura
            record.importe_riesgo = importe_riesgo

    
    
class partner_product_comments(models.Model):
    _name = 'partner.product.comments'

    partner_id = fields.Many2one('res.partner', string="Cliente")
    product_id = fields.Many2one('product.template', string="Producto")
    comments = fields.Text('Comentarios')
    
    
