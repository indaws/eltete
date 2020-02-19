﻿
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)



class WizardPartnerSaleOrder(models.TransientModel):
    _name = 'wizard.partner.sale.order'
    _description = "Crear un pedido para un cliente"
    
    def _default_partner(self):
        return self.env['res.partner'].browse(self._context.get('active_id'))
    
    partner_id = fields.Many2one('res.partner', string="Cliente", required=True, default=_default_partner, readonly=True)
    
    user_id = fields.Many2one('res.users', string="Comercial", default=lambda self: self.env.user, required=True)
    date = fields.Date('Fecha', default=fields.Date.today(), required=True)
    state_id = fields.Many2one('res.country.state', string="Provincia")
    country_id = fields.Many2one('res.country', string="País")
    
    line_ids = fields.One2many('wizard.partner.sale.order.line', 'wizard_id', string="Líneas")
    
    
    
    @api.multi
    def create_sale_order(self): 

        num_pallets = 0
        for line in self.line_ids:
            num_pallets = num_pallets + line.num_pallets
            
        for line in self.line_ids:
        
            if line.referencia_cliente_id.state != 'RCL':
                raise ValidationError("Error: La referencia cliente debe estar en estado REFERENCIA CLIENTE")
        
            #if line.attribute_id.get_price(num_pallets, self.state_id, self.country_id) < 0:
            #    raise ValidationError("Error: No hay ofertas para el atributo " + line.attribute_id.name)
            
            if len(line.lot_ids) > line.num_pallets:
                raise ValidationError("Error: Has introducido más lotes que número de pallets")
            
        customer_payment_mode_id = None
        if self.partner_id.customer_payment_mode_id:
            customer_payment_mode_id = self.partner_id.customer_payment_mode_id.id
            
        property_payment_term_id = None
        if self.partner_id.property_payment_term_id:
            property_payment_term_id = self.partner_id.property_payment_term_id.id
            
        property_delivery_carrier_id = None
        if self.partner_id.property_delivery_carrier_id:
            property_delivery_carrier_id = self.partner_id.property_delivery_carrier_id.id
        
        
        sale = self.env['sale.order'].create({'partner_id': self.partner_id.id, 
                                              'date_order':self.date, 
                                              'user_id': self.user_id.id,
                                              'payment_mode_id': customer_payment_mode_id,
                                              'payment_term_id': property_payment_term_id,
                                              'carrier_id': property_delivery_carrier_id
                                            })
        
        for line in self.line_ids:
            sale.create_sale_order_line_referencia(line.product_id, line.lot_ids, line.referencia_cliente_id, line.attribute_id, line.oferta_id, line.num_pallets)
            
                
            
    
        return {
            'type': 'ir.actions.act_window',
            'name': "Pedido",
            'res_model': 'sale.order',
            'res_id': sale.id, ### Un Solo ID
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'target': 'current',
            #'target': 'new',
            'nodestroy': True,
        }
    
    
    
    

    @api.multi
    def create_sale_order_old(self): 

        num_pallets = 0
        for line in self.line_ids:
            num_pallets = num_pallets + line.num_pallets
            
        for line in self.line_ids:
        
            if line.referencia_cliente_id.state != 'RCL':
                raise ValidationError("Error: La referencia cliente debe estar en estado REFERENCIA CLIENTE")
        
            #if line.attribute_id.get_price(num_pallets, self.state_id, self.country_id) < 0:
            #    raise ValidationError("Error: No hay ofertas para el atributo " + line.attribute_id.name)
            
            if len(line.lot_ids) > line.num_pallets:
                raise ValidationError("Error: Has introducido más lotes que número de pallets")
            
        customer_payment_mode_id = None
        if self.partner_id.customer_payment_mode_id:
            customer_payment_mode_id = self.partner_id.customer_payment_mode_id.id
            
        property_payment_term_id = None
        if self.partner_id.property_payment_term_id:
            property_payment_term_id = self.partner_id.property_payment_term_id.id
            
        property_delivery_carrier_id = None
        if self.partner_id.property_delivery_carrier_id:
            property_delivery_carrier_id = self.partner_id.property_delivery_carrier_id.id
        
        
        sale = self.env['sale.order'].create({'partner_id': self.partner_id.id, 
                                              'date_order':self.date, 
                                              'user_id': self.user_id.id,
                                              'payment_mode_id': customer_payment_mode_id,
                                              'payment_term_id': property_payment_term_id,
                                              'carrier_id': property_delivery_carrier_id
                                            })
        
        for line in self.line_ids:
        
            #i = 0
            #while i < line.num_pallets:
            #    i = i+1
            
            referencia_id = None
            pallet_especial_id = None
            cantonera_color_id = None
            cantonera_forma_id = None
            cantonera_especial_id = None
            cantonera_impresion_id = None
            perfilu_color_id = None
            inglete_id = None
            plancha_color_id = None
            papel_calidad_id = None
            troquelado_id = None
            fsc_id = None
            reciclable_id = None
            
            if line.referencia_cliente_id.referencia_id:
                referencia_id = line.referencia_cliente_id.referencia_id.id
                
            if line.referencia_cliente_id.pallet_especial_id:
                pallet_especial_id = line.referencia_cliente_id.pallet_especial_id.id
                
            if line.attribute_id.cantonera_color_id:
                cantonera_color_id = line.attribute_id.cantonera_color_id.id
                
            if line.attribute_id.cantonera_forma_id:
                cantonera_forma_id = line.attribute_id.cantonera_forma_id.id
                
            if line.attribute_id.cantonera_especial_id:
                cantonera_especial_id = line.attribute_id.cantonera_especial_id.id
                
            if line.attribute_id.cantonera_impresion_id:
                cantonera_impresion_id = line.attribute_id.cantonera_impresion_id.id
                
            if line.attribute_id.perfilu_color_id:
                perfilu_color_id = line.attribute_id.perfilu_color_id.id
                
            if line.attribute_id.inglete_id:
                inglete_id = line.attribute_id.inglete_id.id
                
            if line.attribute_id.plancha_color_id:
                plancha_color_id = line.attribute_id.plancha_color_id.id
                
            if line.attribute_id.papel_calidad_id:
                papel_calidad_id = line.attribute_id.papel_calidad_id.id
                
            if line.attribute_id.troquelado_id:
                troquelado_id = line.attribute_id.troquelado_id.id
                
            if line.attribute_id.fsc_id:
                fsc_id = line.attribute_id.fsc_id.id
                
            if line.attribute_id.reciclable_id:
                reciclable_id = line.attribute_id.reciclable_id.id
            
            
            product_id = None
            for prod in self.env['product.template'].search([('referencia_id', '=', line.referencia_cliente_id.referencia_id.id),
                                                             ('cantonera_color_id', '=', cantonera_color_id),
                                                             ('cantonera_forma_id', '=', cantonera_forma_id),
                                                             ('cantonera_especial_id', '=', cantonera_especial_id),
                                                             ('cantonera_impresion_id', '=', cantonera_impresion_id),
                                                             ('perfilu_color_id', '=', perfilu_color_id),
                                                             ('inglete_id', '=', inglete_id),
                                                             ('inglete_num', '=', line.attribute_id.inglete_num),
                                                             ('plancha_color_id', '=', plancha_color_id),
                                                             ('papel_calidad_id', '=', papel_calidad_id),
                                                             ('troquelado_id', '=', troquelado_id),
                                                             ('fsc_id', '=', fsc_id),
                                                             ('reciclable_id', '=', reciclable_id),
                                                             ]):
                product_id = prod
                
            if product_id == None:
                product_id = self.env['product.template'].create({'name': line.referencia_cliente_id.name + ', ' + line.attribute_id.name, 
                                                                  'type': 'product',
                                                                  'purchase_ok': False,
                                                                  'sale_ok': True,
                                                                  'tracking': 'serial',
                                                                  'categ_id': line.referencia_cliente_id.type_id.id,
                                                                  'attribute_id':line.attribute_id.id, 
                                                                  'referencia_id':line.referencia_cliente_id.referencia_id.id, 
                                                                  'referencia_cliente_id':line.referencia_cliente_id.id, 
                                                                  'cantonera_color_id': cantonera_color_id,
                                                                  'cantonera_forma_id': cantonera_forma_id,
                                                                  'cantonera_especial_id': cantonera_especial_id,
                                                                  'cantonera_impresion_id': cantonera_impresion_id,
                                                                  'perfilu_color_id': perfilu_color_id,
                                                                  'inglete_id': inglete_id,
                                                                  'inglete_num': line.attribute_id.inglete_num,
                                                                  'plancha_color_id': plancha_color_id,
                                                                  'papel_calidad_id': papel_calidad_id,
                                                                  'troquelado_id': troquelado_id,
                                                                  'fsc_id': fsc_id,
                                                                  'reciclable_id': reciclable_id,
                                                                  'cantonera_1': line.attribute_id.cantonera_1,
                                                                  'cantonera_2': line.attribute_id.cantonera_2,
                                                                  'cantonera_3': line.attribute_id.cantonera_3,
                                                                  'cantonera_4': line.attribute_id.cantonera_4,
                                                                  'sierra': line.attribute_id.sierra,
                                                                 })
            
            
            if len(line.lot_ids) > 0 and line.product_id.id == product_id.id:
            
                sale_line = self.env['sale.order.line'].create({'order_id': sale.id, 
                                                    'name':product_id.name, 
                                                    'product_uom_qty': line.num_pallets,
                                                    'price_unit': line.oferta_id.cantidad * line.oferta_id.precio,
                                                    'oferta_precio': line.oferta_id.precio,
                                                    'oferta_precio_tipo': line.oferta_id.precio_tipo,
                                                    'oferta_cantidad': line.oferta_id.cantidad,
                                                    'oferta_cantidad_tipo': line.oferta_id.cantidad_tipo,
                                                    'oferta_unidades': line.oferta_id.unidades,
                                                    'customer_lead': 1,
                                                    'product_uom': 1,
                                                    'oferta_id': line.oferta_id.id,
                                                    'product_id': product_id.product_variant_id.id,
                                                   })
                sale_line._compute_tax_id()
                for lot in line.lot_ids:
                    lot.sale_order_line_id = sale_line.id
            else:
                
                #CREAMOS LÍNEA DE LOTES
                quantity = len(line.lot_ids)
                if quantity > 0:
                    sale_line = self.env['sale.order.line'].create({'order_id': sale.id, 
                                                        'name':product_id.name, 
                                                        'product_uom_qty': quantity,
                                                        'price_unit': line.oferta_id.cantidad * line.oferta_id.precio,
                                                        'oferta_precio': line.oferta_id.precio,
                                                        'oferta_precio_tipo': line.oferta_id.precio_tipo,
                                                        'oferta_cantidad': line.oferta_id.cantidad,
                                                        'oferta_cantidad_tipo': line.oferta_id.cantidad_tipo,
                                                        'oferta_unidades': line.oferta_id.unidades,
                                                        'customer_lead': 1,
                                                        'product_uom': 1,
                                                        'oferta_id': line.oferta_id.id,
                                                        'product_id': line.product_id.product_variant_id.id,
                                                       })
                    sale_line._compute_tax_id()
                    for lot in line.lot_ids:
                        lot.sale_order_line_id = sale_line.id
                                                   
                quantity2 = line.num_pallets - quantity
                if quantity2 > 0:
                    sale_line = self.env['sale.order.line'].create({'order_id': sale.id, 
                                                        'name':product_id.name, 
                                                        'product_uom_qty': quantity2,
                                                        'price_unit': line.oferta_id.cantidad * line.oferta_id.precio,
                                                        'oferta_precio': line.oferta_id.precio,
                                                        'oferta_precio_tipo': line.oferta_id.precio_tipo,
                                                        'oferta_cantidad': line.oferta_id.cantidad,
                                                        'oferta_cantidad_tipo': line.oferta_id.cantidad_tipo,
                                                        'oferta_unidades': line.oferta_id.unidades,
                                                        'customer_lead': 1,
                                                        'product_uom': 1,
                                                        'oferta_id': line.oferta_id.id,
                                                        'product_id': product_id.product_variant_id.id,
                                                       })
                    sale_line._compute_tax_id()
                
            
    
        return {
            'type': 'ir.actions.act_window',
            'name': "Pedido",
            'res_model': 'sale.order',
            'res_id': sale.id, ### Un Solo ID
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'target': 'current',
            #'target': 'new',
            'nodestroy': True,
        }
    
    
    
class WizardPartnerSaleOrder(models.TransientModel):
    _name = 'wizard.partner.sale.order.line'
    
    def _default_partner(self):
        return self.env['res.partner'].browse(self._context.get('active_id'))


    
    partner_id = fields.Many2one('res.partner', string='Cliente', default=_default_partner, readonly=True)
    state_id = fields.Many2one('res.country.state', string="Provincia", related='wizard_id.state_id', store=True, readonly=True)
    country_id = fields.Many2one('res.country', string="País", related='wizard_id.country_id', store=True, readonly=True)
    wizard_id = fields.Many2one('wizard.partner.sale.order', string="Wizard", required=True)
    type_id = fields.Many2one('product.category', string='Tipo', required=True)
    product_id = fields.Many2one('product.template', string='Producto')
    lot_ids = fields.Many2many('stock.production.lot', string="Lotes")
    referencia_cliente_id = fields.Many2one('sale.referencia.cliente', string='Referencia cliente', required=True)
    attribute_id = fields.Many2one('sale.product.attribute', string="Atributo producto", required=True)
    
    num_pallets = fields.Integer(string="Num pallets")
    
    oferta_id = fields.Many2one('sale.offer.oferta', string="Oferta", required=True)
    
    
    
    
class WizardSaleCreateLine(models.TransientModel):
    _name = 'wizard.sale.create.line'
    

        
    def _default_sale(self):
        return self.env['sale.order'].browse(self._context.get('active_id'))


    sale_id = fields.Many2one('sale.order', string='Pedido', default=_default_sale, readonly=True)
    partner_id = fields.Many2one('res.partner', string='Cliente', readonly=True, related='sale_id.partner_id')
    type_id = fields.Many2one('product.category', string='Tipo', )
    product_id = fields.Many2one('product.template', string='Producto')
    lot_ids = fields.Many2many('stock.production.lot', string="Lotes")
    referencia_cliente_id = fields.Many2one('sale.referencia.cliente', string='Referencia cliente')
    attribute_id = fields.Many2one('sale.product.attribute', string="Atributo producto")
    num_pallets = fields.Integer(string="Num pallets", default=1)
    oferta_id = fields.Many2one('sale.offer.oferta', string="Oferta")
    
    
    @api.multi
    def add_lines_sale_order(self): 
        for record in self:
            record.sale_id.create_sale_order_line_referencia(record.product_id, record.lot_ids, record.referencia_cliente_id, record.attribute_id, record.oferta_id, record.num_pallets)

    
    
    
class WizardPurchaseCreateLine(models.TransientModel):
    _name = 'wizard.purchase.create.line'
    

        
    def _default_purchase(self):
        return self.env['purchase.order'].browse(self._context.get('active_id'))


    purchase_id = fields.Many2one('purchase.order', string='Pedido', default=_default_purchase, readonly=True, required=True)
    partner_id = fields.Many2one('res.partner', string='Cliente', required=True )
    referencia_cliente_id = fields.Many2one('sale.referencia.cliente', string='Referencia cliente', required=True)
    attribute_id = fields.Many2one('sale.product.attribute', string="Atributo producto", required=True)
    num_pallets = fields.Integer(string="Num pallets", default=1, required=True)
    oferta_id = fields.Many2one('sale.offer.oferta', string="Oferta", required=True)
    
    
    @api.multi
    def add_lines_purchase_order(self): 
        for record in self:
            record.purchase_id.create_purchase_order_line_referencia(record.partner_id, record.referencia_cliente_id, record.attribute_id, record.oferta_id, record.num_pallets)

    
    
    
    
    

    
    