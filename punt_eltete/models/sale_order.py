
from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    oferta_id = fields.Many2one('sale.offer.oferta', string="Oferta")

    lot_ids = fields.One2many('stock.production.lot', 'sale_order_line_id', string="Lotes")
    
    oferta_precio = fields.Float('Precio', digits = (12,4), readonly = True)
    oferta_precio_tipo = fields.Char('Precio Tipo', readonly = True)
    oferta_cantidad = fields.Float('Cantidad', digits = (12,4), readonly = True)
    oferta_cantidad_tipo = fields.Char('Cantidad Tipo', readonly = True)
    oferta_unidades = fields.Integer('Unidades Pallet')
    
    #precio unitario = cantidad * precio
    
    @api.depends('attribute_ids',)
    def _get_lots_sale(self):
        self.oferta_ids = self.env['stock.production.lot'].search([('sale_order_line_id.order_id', '=', lista_ids)])
    
    
    
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    pedido_cliente = fields.Char('Número Pedido Cliente')
    fecha_entrega = fields.Date('Fecha Entrega Bemeco')
    
    fecha_cliente = fields.Date('Fecha del Pedido Cliente')
    fecha_entrega_cliente = fields.Date('Fecha Entrega del Pedido Cliente')
    
    lot_ids = fields.Many2many('stock.production.lot', compute="_get_lots_sale", string="Lotes")
    
    @api.depends('order_line',)
    def _get_lots_sale(self):
        for record in self:
            record.lot_ids = self.env['stock.production.lot'].search([('sale_order_id', '=', self.id)])
    
    num_pallets = fields.Integer('Num pallets', compute="_get_num_pallets")
    
    @api.depends('order_line.product_uom_qty', 'order_line')
    def _get_num_pallets(self):
    
        for record in self:
            num_pallets = 0
            for line in record.order_line:
                num_pallets = num_pallets + int(line.product_uom_qty)
            record.num_pallets = num_pallets
    
    
    
    @api.multi
    def procesar_fabricacion(self):
        for record in self:
        
            #ubic produccion
            location_id = 7
            
            #ubic stock
            location_dest_id = 12
        
            for line in record.lot_ids:
                if line.fabricado == False:
                    mov_id = self.env['stock.move'].create({'name': 'FABRICACION PEDIDO ' + record.name,
                                                            'product_id': line.product_id.id,
                                                            'product_uom': line.product_id.uom_id.id,
                                                            'product_uom_qty': 1,
                                                            'date': fields.Date.today(),
                                                            'state': 'confirmed',
                                                            'location_id': location_id,
                                                            'location_dest_id': location_dest_id,
                                                            'move_line_ids': [(0, 0, {
                                                                'product_id': line.product_id.id,
                                                                'lot_id': line.id,
                                                                'product_uom_qty': 0,  # bypass reservation here
                                                                'product_uom_id': line.product_id.uom_id.id,
                                                                'qty_done': 1,
                                                                #'package_id': out and self.package_id.id or False,
                                                                #'result_package_id': (not out) and self.package_id.id or False,
                                                                'location_id': location_id,
                                                                'location_dest_id': location_dest_id,
                                                                'owner_id': record.partner_id.id,
                                                            })]
                                                           })
                    line.fabricado = True
                    mov_id._action_done()
                
    
    
    @api.multi
    def enviar_a_fabricar(self):
        for record in self:
            lista_lotes = []
            for line in record.order_line:
            
                cantidad_a_fabricar = int(line.product_uom_qty) - len(line.lot_ids)

                i = 0
                if cantidad_a_fabricar > 0:
                    while i < cantidad_a_fabricar:
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
                                                            'unidades': line.oferta_id.unidades,
                                                            'fabricado': False,
                                                            'sale_order_line_id': line.id

                                                           })
                                lista_lotes.append(lot_id.id)
                    
                            #Asignamos stock a lotes
                line.fabricado = True
                

                
                            
                
                
    @api.multi
    def borrar_fabricacion(self):
        for record in self:
            for line in record.lot_ids:

                x=1
                #Corregimos stock
                
                #Ponemos fabricado a 0
        
    

