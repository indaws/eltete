
from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    
    oferta_id = fields.Many2one('sale.offer.oferta', string="Oferta")
    fabricado = fields.Boolean('Fabricado', readonly=True)
    
    oferta_precio = fields.Float('Precio', digits = (12,4), readonly = True)
    oferta_precio_tipo = fields.Char('Precio Tipo', readonly = True)
    oferta_cantidad = fields.Float('Cantidad', digits = (12,4), readonly = True)
    oferta_cantidad_tipo = fields.Char('Cantidad Tipo', readonly = True)
    oferta_unidades = fields.Integer('Unidades Pallet')
    
    #precio unitario = cantidad * precio
    
    
    
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    fecha_cliente = fields.Date('Fecha Cliente')
    fecha_entrega_cliente = fields.Date('Fecha Entrega Cliente')
    pedido_cliente = fields.Char('Pedido Cliente')
    fecha_entrega = fields.Date('Fecha Entrega')
    
    lot_ids = fields.Many2many('stock.production.lot', string="Lotes", readonly=True)
    
    @api.multi
    def enviar_a_fabricar(self):
        for record in self:
            lista_lotes = []
            for line in record.order_line:

                if line.fabricado == False:
                
                    i = 0
                    while i < line.product_uom_qty:
                        i = i+1
                
                        if line.product_id:
                            if line.product_id.referencia_cliente_id:
                            
                                pallet_especial_id = None
                                if line.product_id.referencia_cliente_id.pallet_especial_id:
                                    pallet_especial_id = line.product_id.referencia_cliente_id.pallet_especial_id.id
                                
                    
                                #Creamos lotes
                                lot_id = self.env['stock.production.lot'].create({'product_id': line.product_id.id, 
                                                            'name': self.env['ir.sequence'].next_by_code('stock.lot.serial'), 
                                                            'pallet_especial_id': pallet_especial_id,
                                                            'ancho_pallet': line.product_id.referencia_cliente_id.ancho_pallet,
                                                            'und_paquete': line.product_id.referencia_cliente_id.und_paquete,
                                                            'paquetes_fila': line.product_id.referencia_cliente_id.paquetes_fila,
                                                            'alto_fila': line.product_id.referencia_cliente_id.alto_fila,
                                                            'fila_max': line.product_id.referencia_cliente_id.fila_max,
                                                            'fila_buena': line.product_id.referencia_cliente_id.fila_buena,
                                                            #'unidades': line.product_id.,
                                                            'fabricado': True,

                                                           })
                                lista_lotes.append(lot_id.id)
                        
                                #Asignamos stock a lotes
                line.fabricado = True
                
            #Añadimos lotes al pedido
            if len(lista_lotes) > 0:
                record.write({'lot_ids': [( 6, 0, lista_lotes)]})
                
                            
                
                
    @api.multi
    def borrar_fabricacion(self):
        for record in self:
            for line in record.lot_ids:

                x=1
                #Corregimos stock
                
                #Ponemos fabricado a 0
        
    

