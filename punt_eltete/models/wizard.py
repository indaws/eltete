
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
    num_pallets = fields.Integer(string="Num pallets")
    oferta_id = fields.Many2one('sale.offer.oferta', string="Oferta")
    
    importe_riesgo = fields.Float('RIESGO PERMITIDO', digits = (12, 2), readonly = True, compute="_get_riesgo")
    
    @api.multi
    def add_lines_sale_order(self): 
        for record in self:
            record.sale_id.create_sale_order_line_referencia(record.product_id, record.lot_ids, record.referencia_cliente_id, record.attribute_id, record.oferta_id, record.num_pallets)

   @api.multi
    def _get_riesgo(self): 
        for record in self: 
            importe_riesgo = 0
            if record.partner_id:
                importe_riesgo = partner_id.importe_riesgo
            record.importe_riesgo = importe_riesgo
    
    
class WizardPurchaseCreateLine(models.TransientModel):
    _name = 'wizard.purchase.create.line'
    

        
    def _default_purchase(self):
        return self.env['purchase.order'].browse(self._context.get('active_id'))


    purchase_id = fields.Many2one('purchase.order', string='Pedido', default=_default_purchase, readonly=True, required=True)
    partner_id = fields.Many2one('res.partner', string='Cliente', required=True )
    line_id = fields.Many2one('sale.order.line', string="Línea pedido de venta")
    
    #referencia_cliente_id = fields.Many2one('sale.referencia.cliente', string='Referencia cliente', required=True)
    #attribute_id = fields.Many2one('sale.product.attribute', string="Atributo producto", required=True)
    num_pallets = fields.Integer(string="Num pallets", default=1, required=True)
    #oferta_id = fields.Many2one('sale.offer.oferta', string="Oferta", required=True)
    
    
    @api.multi
    def add_lines_purchase_order(self): 
        for record in self:
            record.purchase_id.create_purchase_order_line_referencia(record.partner_id, record.line_id, record.num_pallets)

    
    
    
    
    

    
    
