
from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    lot_ids = fields.One2many('stock.production.lot', 'sale_order_line_id', string="Lotes")
    
    oferta_precio = fields.Float('Precio', digits = (12,4), readonly = True)
    oferta_precio_tipo = fields.Char('Precio Tipo', readonly = True)
    oferta_cantidad = fields.Float('Cantidad', digits = (12,4), readonly = True)
    oferta_cantidad_tipo = fields.Char('Cantidad Tipo', readonly = True)
    oferta_unidades = fields.Integer('Unidades Pallet')
    
    #Campos visibles
    #referencia_cliente_id = fields.Many2one('sale.referencia.cliente', string='Referencia cliente', ondelete='cascade')
    #attribute_id = fields.Many2one('sale.product.attribute', string="Atributo producto", required=True, ondelete='cascade')
    oferta_id = fields.Many2one('sale.offer.oferta', string="Oferta", required = True)
    num_pallets = fields.Integer('Número de Pallets', default = 1, required = True)
    precio = fields.Float('Precio', digits = (12, 4), readonly = True, compute = "_get_valores")
    importe = fields.Float('Importe', readonly = True, digits = (10, 2), compute = "_get_valores")
    
    #Son visibles en el pdf
    codigo_cliente = fields.Char('Código', readonly = True, compute = "_get_valores")
    descripcion = fields.Html('Descripción', readonly = True, compute = "_get_valores")
    und_pallet = fields.Integer('Unidades Pallet', readonly = True, compute = "_get_valores")
    cantidad = fields.Html('Cantidad', readonly = True, compute = "_get_valores")
    
    #No son visibles
    peso_neto = fields.Integer('Peso Neto', readonly = True, compute = "_get_valores")
    peso_bruto = fields.Integer('Peso Bruto', readonly = True, compute = "_get_valores")
    eton = fields.Float('Eton Medio', digits = (8, 1), readonly = True, compute = "_get_valores")
    
    
    @api.depends('oferta_id', 'num_pallets')
    def _get_valores(self):
        for record in self:
            codido = ""
            descripcion = ""
            und_pallet = 0
            cantidad = ""
            precio = ""
            importe = 0
            peso_neto = 0
            peso_bruto = 0
            eton = 0

            codigo = record.oferta_id.attribute_id.codigo_cliente
            
            descripcion = record.oferta_id.attribute_id.titulo + "<br/>"
            descripcion = descripcion + record.oferta_id.attribute_id.referencia_cliente_id.referencia_cliente_nombre + "<br/>"
            descripcion = descripcion + record.oferta_id.attribute_id.descripcion
            
            und_pallet = record.oferta_id.unidades
            
            cantidad_total = record.oferta_id.cantidad * record.num_pallets * 10000
            
            
            decimales = 4
            while cantidad_total % 10 == 0 and decimales > 0:
                cantidad_total = cantidad_total / 10
                decimales = decimales - 1
            cantidad = str(cantidad_total) + "<br/>" + record.oferta_id.cantidad_tipo
            
            
            precio = record.oferta_id.precio + "<br/>" + record.oferta_id.precio_tipo
            
            importe = int(precio * cantidad_total * 100) / 100
            
            peso_neto = record.und_pallet * record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro * record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
            toneladas = peso_neto / 1000
            
            eton = record.oferta_id.precio_eton
            
            peso_bruto = peso_neto
            pesoMadera = 0
            if record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud < 1500:
                pesoMadera = 20
            elif record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud < 2000:
                pesoMadera = 30
            else:
                pesoMadera = int(self.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud / 1000) * 20
                
            peso_bruto = int((peso_bruto + pesoMadera) / 5) * 5
            peso_neto = int(peso_neto / 5) * 5
            
            record.codigo = codigo
            record.descripcion = descripcion
            record.und_pallet = und_pallet
            record.cantidad = cantidad
            record.precio = precio
            record.price_subtotal = importe
            record.price_unit = eton
            record.product_uom_qty = toneladas
            record.peso_neto = peso_neto
            record.peso_bruto = peso_bruto
            record.eton = eton
    
    
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
    

    num_pallets = fields.Integer('Pallets Pedido', compute="_get_num_pallets")
    peso_neto = fields.Integer('Peso Neto', compute="_get_num_pallets")
    peso_bruto = fields.Integer('Peso Bruto', compute="_get_num_pallets")
    toneladas = fields.Float('Toneladas', digits = (8, 1), compute="_get_num_pallets")
    eton = fields.Float('Eton', digits = (8, 1), compute="_get_num_pallets")
    
    
    @api.depends('order_line',)
    def _get_lots_sale(self):
        for record in self:
            record.lot_ids = self.env['stock.production.lot'].search([('sale_order_id', '=', self.id)])

            
            
    @api.depends('order_line.num_pallets', 'order_line.peso_neto', 'order_line.peso_bruto', 'order_line.product_uom_qty', 'order_line.eton', 'order_line')
    def _get_num_pallets(self):
    
        for record in self:
            num_pallets = 0
            peso_neto = 0
            peso_bruto = 0
            toneladas = 0
            eton_total = 0
            
            for line in record.order_line:
                #num_pallets = num_pallets + int(line.product_uom_qty)
                num_pallets = num_pallets + int(line.num_pallets)
                peso_neto = peso_pedido + line.peso_neto
                peso_bruto = peso_pedido + line.peso_bruto
                toneladas = toneladas + line.product_uom_qty
                eton_total = eton_total + line.eton * line.product_uom_qty

            eton_medio = 0
            if toneladas > 0:
                eton_medio = eton_total / toneladas
            eton_medio = int(eton_medio * 10) / 10
            toneladas = int(toneladas * 10) / 10
            
            record.peso_neto = peso_neto
            record.peso_bruto = peso_bruto
            record.toneladas = toneladas
            record.eton = eton_medio

            record.num_pallets = num_pallets

    
    @api.multi
    def procesar_fabricacion(self):
        for record in self:
        
            #ubic produccion
            location_id = 7
            
            #ubic stock
            location_dest_id = 13
        
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
        
    

