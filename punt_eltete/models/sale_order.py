from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    lot_ids = fields.One2many('stock.production.lot', 'sale_order_line_id', string="Lotes")
    
    oferta_precio = fields.Float('Precio Julio', digits = (12,4))
    oferta_precio_tipo = fields.Char('Precio Tipo Julio')
    oferta_cantidad = fields.Float('Cantidad Julio', digits = (12,4))
    oferta_cantidad_tipo = fields.Char('Cantidad Tipo Julio')
    oferta_unidades = fields.Integer('Unidades Pallet julio')
    
    #Campos visibles
    #referencia_cliente_id = fields.Many2one('sale.referencia.cliente', string='Referencia cliente', ondelete='cascade')
    #attribute_id = fields.Many2one('sale.product.attribute', string="Atributo producto", required=True, ondelete='cascade')
    oferta_id = fields.Many2one('sale.offer.oferta', string="Oferta")
    und_user = fields.Integer('Unidades Pallet Fabricadas', default = -1)
    kilos_user = fields.Integer('kilos Pallet Fabricados', default = -1)
    num_pallets = fields.Integer('Número de Pallets', default = 1)
    BULTOS_SEL = [('1', 'SI'),     
                  ('2', 'NO'),
                  ]
    bultos = fields.Selection(selection = BULTOS_SEL, string = 'Es pallet', default='1')
    
    #Campos calculados
    codigo_cliente = fields.Char('Código cliente', readonly = True, compute = "_get_valores")
    descripcion = fields.Html('Descripción', readonly = True, compute = "_get_valores")
    und_pallet = fields.Integer('Unidades Pallet', readonly = True, compute = "_get_valores")
    cantidad = fields.Char('Cantidad', compute = "_get_valores")
    precio = fields.Char('Precio', readonly = True, compute = "_get_valores")
    importe = fields.Float('Importe', digits = (10,2), readonly = True, compute = "_get_valores")
    peso_neto = fields.Integer('Peso Neto Pallet', readonly = True, compute = "_get_valores")
    peso_bruto = fields.Integer('Peso Bruto Pallet', readonly = True, compute = "_get_valores")
    
    ESTADO_SEL = [('0', 'NO CONFIRMADO - FALTA PAPEL'),    
                  ('1', 'NO CONFIRMADO - FALTA CLICHE'),
                  ('2', 'NO CONFIRMADO - FALTA TINTA'),
                  ('3', 'NO CONFIRMADO - PARA FABRICAR'),

                  ('7', 'NO CONFIRMADO - HAY QUE COMPRAR'),
                  ('8', 'NO CONFIRMADO - COMPRADO'),
                  ('9', 'NO CONFIRMADO - HAY STOCK'),
                  
                  ('10', 'CONFIRMADO - FALTA PAPEL'),
                  ('11', 'CONFIRMADO - FALTA CLICHE'),
                  ('12', 'CONFIRMADO - FALTA TINTA'),
                  ('13', 'CONFIRMADO - PARA FABRICAR'),
                  ('14', 'CONFIRMADO - FABRICANDO'),
                  ('15', 'CONFIRMADO - FALTA CORTAR'),
                  ('16', 'CONFIRMADO - FABRICADO'),
                  ('17', 'CONFIRMADO - HAY QUE COMPRAR'),
                  ('18', 'CONFIRMADO - COMPRADO'),
                  ('19', 'CONFIRMADO - HAY STOCK'),
                  
                  ('20', 'LISTO'),
                  ]
    estado = fields.Selection(selection = ESTADO_SEL, string = 'Estado')
    
    ancho_interior = fields.Char('Ancho Interior', readonly = True, compute = "_get_fabricacion")
    ancho_superficie = fields.Char('Ancho Superficie', readonly = True, compute = "_get_fabricacion")
    j_gram = fields.Integer('J Gram', readonly = True, compute = "_get_fabricacion")
    j_interior = fields.Integer('J Interior', readonly = True, compute = "_get_fabricacion")
    j_superficie = fields.Integer('J Superficie', readonly = True, compute = "_get_fabricacion")
    j_superficie_max = fields.Integer('J Superficie Max', readonly = True, compute = "_get_fabricacion")
    comentario_paletizado = fields.Text('Comentario Paletizado', readonly = True, compute = "_get_fabricacions")
    
    
    @api.onchange('oferta_id', 'num_pallets', 'und_user', 'kilos_user' )
    def _onchange_oferta_cantidad(self):
        if self.num_pallets > 0:
            self.price_unit = self.importe / self.num_pallets
        self.product_uom_qty = self.num_pallets
    
    @api.depends('oferta_id', 'num_pallets', 'und_user', 'kilos_user')
    def _get_valores(self):
        for record in self:
            codigo_cliente = record.oferta_id.attribute_id.codigo_cliente
            descripcion = ''
            if record.oferta_id:
                descripcion = record.oferta_id.attribute_id.referencia_cliente_id.name + " " + record.oferta_id.attribute_id.name
            und_pallet = 0
            cantidad = ""
            precio = ""
            importe = 0
            peso_neto = 0
            peso_bruto = 0

            if record.und_user > 0:
                und_pallet = record.und_user
            else:
                und_pallet = record.oferta_id.unidades
            
            facturar = record.oferta_id.attribute_id.referencia_cliente_id.precio_cliente
            cantidad_num = 0
            precio_num = 0
            #metros
            if facturar == '1':
                cantidad_num = record.num_pallets * und_pallet * record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
                cantidad_num = int(cantidad_num * 10000) / 10000
                cantidad = str(cantidad_num) + " metros"
                precio_num = record.oferta_id.precio_metro
                precio_num = int(precio_num * 10000) / 10000
                precio = str(precio_num) + " €/metro"
                
                if record.kilos_user > 0:
                    peso_bruto = record.kilos_user
                    peso_neto = peso_bruto - 15
                else:
                    peso_neto = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro * record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
                    peso_neto = peso_neto * und_pallet
                
                    pesoMadera = 0
                    if record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud < 1500:
                        pesoMadera = 15
                    elif record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud < 2000:
                        pesoMadera = 20
                    else:
                        pesoMadera = int(record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud / 1000) * 15
                    peso_bruto = int((peso_neto + pesoMadera) / 5) * 5
            #unidades
            elif facturar == '2':
                cantidad_num = record.num_pallets * und_pallet
                cantidad_num = int(cantidad_num * 10000) / 10000
                cantidad = str(cantidad_num) + " unidades"
                precio_num = record.oferta_id.precio_metro * record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
                precio_num = int(precio_num * 100000) / 100000
                precio = str(precio_num) + " €/unidad"
                
                if record.kilos_user > 0:
                    peso_bruto = record.kilos_user
                    peso_neto = peso_bruto - 15
                else:
                    peso_neto = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro * record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
                    peso_neto = peso_neto * und_pallet
                
                    pesoMadera = 0
                    if record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud < 1500:
                        pesoMadera = 15
                    elif record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud < 2000:
                        pesoMadera = 20
                    else:
                        pesoMadera = int(record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud / 1000) * 15
                    peso_bruto = int((peso_neto + pesoMadera) / 5) * 5
            #Millares
            elif facturar == '3':
                cantidad_num = record.num_pallets * und_pallet / 1000
                cantidad_num = int(cantidad_num * 10000) / 10000
                cantidad = str(cantidad_num) + " millares"
                precio_num = record.oferta_id.precio_metro * record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad * 1000
                precio_num = int(precio_num * 10000) / 10000
                precio = str(precio_num) + " €/millar"
                
                if record.kilos_user > 0:
                    peso_bruto = record.kilos_user
                    peso_neto = peso_bruto - 15
                else:
                    peso_neto = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro * record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
                    peso_neto = peso_neto * und_pallet
                
                    pesoMadera = 0
                    if record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud < 1500:
                        pesoMadera = 15
                    elif record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud < 2000:
                        pesoMadera = 20
                    else:
                        pesoMadera = int(record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud / 1000) * 15
                    peso_bruto = int((peso_neto + pesoMadera) / 5) * 5
            #Kilos
            elif facturar == '4':
                if record.kilos_user > 0:
                    peso_neto = record.kilos_user - 15
                    peso_bruto = record.kilos_user
                else:
                    peso_neto = record.oferta_id.kilos
                    peso_bruto = peso_neto + 15
                cantidad_num = record.num_pallets * peso_neto
                cantidad_num = int(cantidad_num * 10000) / 10000
                cantidad = str(cantidad_num) + " kilos"
                precio_num = record.oferta_id.precio_kilo
                precio_num = int(precio_num * 10000) / 10000
                precio = str(precio_num) + " €/kilo"
            #Varios
            elif facturar == '5':
                cantidad_num = record.num_pallets * und_pallet
                cantidad_num = int(cantidad_num * 10000) / 10000
                cantidad = str(cantidad_num) + " unidades"
                precio_num = record.oferta_id.precio_varios
                precio_num = int(precio_num * 10000) / 10000
                precio = str(precio_num) + " €/unidad"
                peso_neto = 0
                peso_bruto = 0
            
            importe = precio_num * cantidad_num
            
            record.codigo_cliente = codigo_cliente
            record.descripcion = descripcion
            record.und_pallet = und_pallet
            record.cantidad = cantidad
            record.precio = precio
            record.importe = importe
            record.peso_neto = peso_neto
            record.peso_bruto = peso_bruto
            

    def _get_fabricacion(self):
        for record in self:
            record.ancho_interior = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ancho_interior
            record.ancho_superficie = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ancho_superficie
            record.j_gram = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.j_gram
            record.j_interior = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.j_interior
            record.j_superficie = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.j_superficie
            record.j_superficie_max = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.j_superficie_max
            record.comentario_paletizado = record.oferta_id.attribute_id.referencia_cliente_id.comentario_paletizado
    
    
    
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
    
    ESTADOS_SEL = [('0', 'NO CONFIRMADO'),     
                  ('1', 'CONFIRMADO'),
                  ('2', 'FABRICADO'),
                  ('3', 'ENTREGA PARCIAL'),
                  ('4', 'ENTREGA TOTAL'),
                  ]
    estado = fields.Selection(selection = ESTADOS_SEL, string = 'Es pallet', default='1')
    
    
    
    @api.multi
    def create_sale_order_line_referencia(self, line_product_id, lot_ids, referencia_cliente_id, attribute_id, oferta_id, num_pallets):
        for record in self:
        
            #_logger.warning('222')
        
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
            
            if referencia_cliente_id.referencia_id:
                referencia_id = referencia_cliente_id.referencia_id.id
                
            if referencia_cliente_id.pallet_especial_id:
                pallet_especial_id = referencia_cliente_id.pallet_especial_id.id
                
            if attribute_id.cantonera_color_id:
                cantonera_color_id = attribute_id.cantonera_color_id.id
                
            if attribute_id.cantonera_forma_id:
                cantonera_forma_id = attribute_id.cantonera_forma_id.id
                
            if attribute_id.cantonera_especial_id:
                cantonera_especial_id = attribute_id.cantonera_especial_id.id
                
            if attribute_id.cantonera_impresion_id:
                cantonera_impresion_id = attribute_id.cantonera_impresion_id.id
                
            if attribute_id.perfilu_color_id:
                perfilu_color_id = attribute_id.perfilu_color_id.id
                
            if attribute_id.inglete_id:
                inglete_id = attribute_id.inglete_id.id
                
            if attribute_id.plancha_color_id:
                plancha_color_id = attribute_id.plancha_color_id.id
                
            if attribute_id.papel_calidad_id:
                papel_calidad_id = attribute_id.papel_calidad_id.id
                
            if attribute_id.troquelado_id:
                troquelado_id = attribute_id.troquelado_id.id
                
            if attribute_id.fsc_id:
                fsc_id = attribute_id.fsc_id.id
                
            if attribute_id.reciclable_id:
                reciclable_id = attribute_id.reciclable_id.id
            
            
            product_id = None
            for prod in self.env['product.template'].search([('referencia_id', '=', referencia_cliente_id.referencia_id.id),
                                                             ('cantonera_color_id', '=', cantonera_color_id),
                                                             ('cantonera_forma_id', '=', cantonera_forma_id),
                                                             ('cantonera_especial_id', '=', cantonera_especial_id),
                                                             ('cantonera_impresion_id', '=', cantonera_impresion_id),
                                                             ('perfilu_color_id', '=', perfilu_color_id),
                                                             ('inglete_id', '=', inglete_id),
                                                             ('inglete_num', '=', attribute_id.inglete_num),
                                                             ('plancha_color_id', '=', plancha_color_id),
                                                             ('papel_calidad_id', '=', papel_calidad_id),
                                                             ('troquelado_id', '=', troquelado_id),
                                                             ('fsc_id', '=', fsc_id),
                                                             ('reciclable_id', '=', reciclable_id),
                                                             ]):
                product_id = prod
                
            if product_id == None:
                product_id = self.env['product.template'].create({'name': referencia_cliente_id.name + ', ' + attribute_id.name, 
                                                                  'type': 'product',
                                                                  'purchase_ok': False,
                                                                  'sale_ok': True,
                                                                  'tracking': 'serial',
                                                                  'categ_id': referencia_cliente_id.type_id.id,
                                                                  'attribute_id':attribute_id.id, 
                                                                  'referencia_id':referencia_cliente_id.referencia_id.id, 
                                                                  'referencia_cliente_id':referencia_cliente_id.id, 
                                                                  'cantonera_color_id': cantonera_color_id,
                                                                  'cantonera_forma_id': cantonera_forma_id,
                                                                  'cantonera_especial_id': cantonera_especial_id,
                                                                  'cantonera_impresion_id': cantonera_impresion_id,
                                                                  'perfilu_color_id': perfilu_color_id,
                                                                  'inglete_id': inglete_id,
                                                                  'inglete_num': attribute_id.inglete_num,
                                                                  'plancha_color_id': plancha_color_id,
                                                                  'papel_calidad_id': papel_calidad_id,
                                                                  'troquelado_id': troquelado_id,
                                                                  'fsc_id': fsc_id,
                                                                  'reciclable_id': reciclable_id,
                                                                  'cantonera_1': attribute_id.cantonera_1,
                                                                  'cantonera_2': attribute_id.cantonera_2,
                                                                  'cantonera_3': attribute_id.cantonera_3,
                                                                  'cantonera_4': attribute_id.cantonera_4,
                                                                  'sierra': attribute_id.sierra,
                                                                 })
            
            
            if len(lot_ids) > 0 and line_product_id.id == product_id.id:
            
                sale_line = self.env['sale.order.line'].create({'order_id': record.id, 
                                                    'name':product_id.name, 
                                                    'product_uom_qty': num_pallets,
                                                    'num_pallets': num_pallets,
                                                    'price_unit': oferta_id.cantidad * oferta_id.precio,
                                                    'oferta_precio': oferta_id.precio,
                                                    'oferta_precio_tipo': oferta_id.precio_tipo,
                                                    'oferta_cantidad': oferta_id.cantidad * num_pallets,
                                                    'oferta_cantidad_tipo': oferta_id.cantidad_tipo,
                                                    'oferta_unidades': oferta_id.unidades,
                                                    'customer_lead': 1,
                                                    'product_uom': 1,
                                                    'oferta_id': oferta_id.id,
                                                    'product_id': product_id.product_variant_id.id,
                                                   })
                sale_line._compute_tax_id()
                for lot in lot_ids:
                    lot.sale_order_line_id = sale_line.id
            else:
                
                #CREAMOS LÍNEA DE LOTES
                quantity = len(lot_ids)
                if quantity > 0:
                    sale_line = self.env['sale.order.line'].create({'order_id': record.id, 
                                                        'name':product_id.name, 
                                                        'product_uom_qty': quantity,
                                                        'num_pallets': quantity,
                                                        'price_unit': oferta_id.cantidad * oferta_id.precio,
                                                        'oferta_precio': oferta_id.precio,
                                                        'oferta_precio_tipo': oferta_id.precio_tipo,
                                                        'oferta_cantidad': oferta_id.cantidad * quantity,
                                                        'oferta_cantidad_tipo': oferta_id.cantidad_tipo,
                                                        'oferta_unidades': oferta_id.unidades,
                                                        'customer_lead': 1,
                                                        'product_uom': 1,
                                                        'oferta_id': oferta_id.id,
                                                        'product_id': line_product_id.product_variant_id.id,
                                                       })
                    sale_line._compute_tax_id()
                    for lot in lot_ids:
                        lot.sale_order_line_id = sale_line.id
                                                   
                quantity2 = num_pallets - quantity
                if quantity2 > 0:
                    sale_line = self.env['sale.order.line'].create({'order_id': record.id, 
                                                        'name':product_id.name, 
                                                        'product_uom_qty': quantity2,
                                                        'num_pallets': quantity2,
                                                        'price_unit': oferta_id.cantidad * oferta_id.precio,
                                                        'oferta_precio': oferta_id.precio,
                                                        'oferta_precio_tipo': oferta_id.precio_tipo,
                                                        'oferta_cantidad': oferta_id.cantidad * quantity2,
                                                        'oferta_cantidad_tipo': oferta_id.cantidad_tipo,
                                                        'oferta_unidades': oferta_id.unidades,
                                                        'customer_lead': 1,
                                                        'product_uom': 1,
                                                        'oferta_id': oferta_id.id,
                                                        'product_id': product_id.product_variant_id.id,
                                                       })
                    sale_line._compute_tax_id()
    
    
    @api.depends('order_line',)
    def _get_lots_sale(self):
        for record in self:
            record.lot_ids = self.env['stock.production.lot'].search([('sale_order_id', '=', self.id)])

            
            
    @api.depends('order_line.num_pallets', 'order_line.peso_neto', 'order_line.peso_bruto', 'order_line.product_uom_qty', 'order_line.price_unit', 'order_line')
    def _get_num_pallets(self):
    
        for record in self:
            num_pallets = 0
            peso_neto = 0
            peso_bruto = 0

            
            for line in record.order_line:
                if line.bultos == '1':
                    num_pallets = num_pallets + line.num_pallets
                peso_neto = peso_neto + (line.peso_neto * line.num_pallets)
                peso_bruto = peso_bruto + (line.peso_bruto * line.num_pallets)

            
            record.num_pallets = num_pallets
            record.peso_neto = peso_neto
            record.peso_bruto = peso_bruto
            
            record.toneladas = 0
            record.eton = 0

            

    
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
            
                if line.bultos == '1':
            
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

