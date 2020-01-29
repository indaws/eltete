from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    lot_ids = fields.One2many('stock.production.lot', 'sale_order_line_id', string="Lotes")

    attribute_id = fields.Many2one('sale.product.attribute', string="Atributo producto", )
    oferta_id = fields.Many2one('sale.offer.oferta', string="Oferta")
    und_user = fields.Integer('Und Pallet Fabricadas', default = -1)
    kilos_user = fields.Float('kg Pallet Fabricados', digits=(10, 2), default = -1)
    num_pallets = fields.Integer('NUm Pallets', default = 1)
    BULTOS_SEL = [('1', 'SI'),     
                  ('2', 'NO'),
                  ]
    bultos = fields.Selection(selection = BULTOS_SEL, string = 'Es pallet', default='1')
    aclaracion = fields.Char('Aclaración')
    hayaclaracion = fields.Boolean('Hay Aclaración', compute = "_hay_aclaracion")
    no_editar = fields.Boolean('No Editar')
    
    #Campos calculados
    codigo_cliente = fields.Char('Código cliente', readonly = True, compute = "_get_valores")
    descripcion = fields.Html('Descripción', readonly = True, compute = "_get_valores")
    und_pallet = fields.Integer('Unidades Pallet', readonly = True, compute = "_get_valores")
    cantidad = fields.Char('Cantidad', compute = "_get_valores")
    precio = fields.Char('Precio', readonly = True, compute = "_get_valores")
    importe = fields.Float('Importe', digits = (10,2), readonly = True, compute = "_get_valores")
    peso_neto = fields.Integer('Peso Neto Pallet', readonly = True, compute = "_get_valores")
    peso_bruto = fields.Integer('Peso Bruto Pallet', readonly = True, compute = "_get_valores")
    eton = fields.Float('Eton', digits=(8, 1), readonly = True, compute = "_get_valores")
    
    lotes_fabricar = fields.Integer('Lotes Fabricar')
    lotes_inicio = fields.Integer('Lotes Inicio', default = 1)
    
    
    ESTADO_SEL = [('0', 'ESPERANDO'),    
                  ('1', 'MANDAR A FABRICAR'),
                  ('2', 'MANDAR A MANIPULAR'),
                  ('3', 'PREPARAR'),
                  ]
    estado = fields.Selection(selection = ESTADO_SEL, string = 'Estado')
    
    op_cantonera_maquina = fields.Char('Máquina', compute = "_get_produccion")
    op_superficie_color = fields.Char('Superficie Color', compute = "_get_produccion")
    op_superficie_ancho = fields.Char('Superficie Ancho', compute = "_get_produccion")
    op_interior_ancho = fields.Char('Interior Ancho', compute = "_get_produccion")
    op_interior_gramaje = fields.Char('Interior Gramaje', compute = "_get_produccion")
    op_tinta_1 = fields.Char('Tinta 1', compute = "_get_produccion")
    op_texto_1 = fields.Char('Texto 1', compute = "_get_produccion")
    op_tinta_2 = fields.Char('Tinta 2', compute = "_get_produccion")
    op_texto_2 = fields.Char('Texto 2', compute = "_get_produccion")
    op_alas = fields.Char('Alas', compute = "_get_produccion")
    op_grosor = fields.Char('Grosor', compute = "_get_produccion")
    op_longitud = fields.Char('Longitud', compute = "_get_produccion")
    op_tolerancia_alas = fields.Char('Tolerancia Alas', compute = "_get_produccion")
    op_tolerancia_grosor = fields.Char('Tolerancia Grosor', compute = "_get_produccion")
    op_tolerancia_longitud = fields.Char('Tolerancia Longitud', compute = "_get_produccion")
    op_ancho_pallet = fields.Char('Ancho Pallet', compute = "_get_produccion")  
    op_tipo_pallet = fields.Char('Tipo Pallet', compute = "_get_produccion")
    op_paletizado = fields.Char('Paletizado', compute = "_get_produccion")
    op_und_paquete = fields.Char('Unidades Paquete', compute = "_get_produccion")
    op_paquetes_fila= fields.Char('Paquetes Fila', compute = "_get_produccion")
    op_und_exactas = fields.Char('Unidades Exactas', compute = "_get_produccion")
    op_metros = fields.Char('Metros', compute = "_get_produccion")
    op_peso_interior = fields.Char('Peso Interior', compute = "_get_produccion")
    op_peso_superficie = fields.Char('Peso Superficie', compute = "_get_produccion")
    op_duracion = fields.Char('Duración', compute = "_get_produccion")
    op_comentario = fields.Char('Comentario', compute = "_get_produccion")
    op_forma = fields.Char('Forma', compute = "_get_produccion")
    op_especial = fields.Char('Especial', compute = "_get_produccion")
    
    @api.multi
    def action_view_form_sale_order(self):
        view = self.env.ref('sale.sale_order_line_view_form_readonly')
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order.line',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'res_id': self.id,
            'context': self.env.context,
        }
    
    @api.onchange('no_editar',)
    def _onchange_no_editar(self):
        if self.no_editar == True:
            self.attribute_id.write({'no_editar': True})
            self.oferta_id.write({'no_editar': True})
    
    
    @api.onchange('partner_shipping_id',)
    def _onchange_provincia(self):
        self.provincia_id = self.partner_shipping_id.state_id
    

    @api.onchange('lot_ids', 'num_pallets')
    def _onchange_lotes_fabricar(self):
        lotes_fabricar = self.num_pallets - len(self.lot_ids)
        self.lotes_fabricar = lotes_fabricar
    
    
    @api.multi
    def procesar_fabricacion_linea(self):
        for record in self:
            #ubic produccion
            location_id = 7
            #ubic stock
            location_dest_id = 13
        
            for line in record.lot_ids:
                if line.fabricado == False:
                    mov_id = self.env['stock.move'].create({'name': 'FABRICACION PEDIDO ' + record.order_id.name,
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
                                                                'location_id': location_id,
                                                                'location_dest_id': location_dest_id,
                                                                'owner_id': record.order_id.partner_id.id,
                                                            })]
                                                           })
                    line.fabricado = True
                    mov_id._action_done()
                
    
    
    @api.multi
    def enviar_a_fabricar_linea(self):
        for line in self:
            cliente_id = line.order_id.partner_id.id
            if line.order_id.pedido_stock == True:
                cliente_id = None
        
            if line.bultos == '1':
                cantidad_a_fabricar = int(line.product_uom_qty) - len(line.lot_ids)

                if cantidad_a_fabricar > 0:
                    i = 0
                    while i < cantidad_a_fabricar:
                        i = i+1
                
                        if line.product_id:
                            #Creamos lotes
                            lot_id = self.env['stock.production.lot'].create({'product_id': line.product_id.id, 
                                                        'name': self.env['ir.sequence'].next_by_code('stock.lot.serial'), 
                                                        'referencia_id': line.product_id.referencia_id.id, 
                                                        'cliente_id': cliente_id,
                                                        'sale_order_line_id': line.id,
                                                        'fabricado': False,
                                                       })
                    
                            #Asignamos stock a lotes
                line.fabricado = True
    

    
    
    @api.depends('aclaracion')
    def _hay_aclaracion(self):
        for record in self:
            hayaclaracion = False
            if record.aclaracion and len(record.aclaracion) > 0:
                hayaclaracion = True
            record.hayaclaracion = hayaclaracion
    
    
    
    @api.depends('oferta_id', 'und_pallet', 'num_pallets')
    def _get_produccion(self):
        for record in self:
            maquina = ""
            if record.oferta_id.attribute_id.cantonera_1 == True:
                maquina = maquina + "Línea 1, "
            if record.oferta_id.attribute_id.cantonera_2 == True:
                maquina = maquina + "Línea 2, "
            if record.oferta_id.attribute_id.cantonera_3 == True:
                maquina = maquina + "Línea 3, "
            if record.oferta_id.attribute_id.cantonera_4 == True:
                maquina = maquina + "Línea 4, "
            
            superficie_color = ""
            if record.oferta_id.attribute_id.cantonera_color_id:
                superficie_color = record.oferta_id.attribute_id.cantonera_color_id.name
            superficie_ancho = "" 
            if record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ancho_superficie:
                superficie_ancho = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ancho_superficie
            interior_ancho = ""
            if record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ancho_interior:
                interior_ancho = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ancho_interior 
            aux1 = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.j_gram
            aux2 = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.j_gram + 100
            interior_gramaje = str(aux1) + " - " + str(aux2)
            
            tintero1 = False
            tintero2 = False
            tinta_1 = ""
            texto_1 = ""
            tinta_2 = ""
            texto_2 = ""
            if record.oferta_id.attribute_id.cantonera_cliche_id:
                if record.oferta_id.attribute_id.cantonera_cliche_id.tinta_1_id:
                    tinta_1 = record.oferta_id.attribute_id.cantonera_cliche_id.tinta_1_id.name
                    tintero1 = True
                    if record.oferta_id.attribute_id.cantonera_cliche_id.texto_1:
                        texto_1 = record.oferta_id.attribute_id.cantonera_cliche_id.texto_1
                if record.oferta_id.attribute_id.cantonera_cliche_id.tinta_2_id:
                    if tintero1 == False:
                        tinta_1 = record.oferta_id.attribute_id.cantonera_cliche_id.tinta_2_id.name
                        tintero1 = True
                        if record.oferta_id.attribute_id.cantonera_cliche_id.texto_2:
                            texto_1 = record.oferta_id.attribute_id.cantonera_cliche_id.texto_2
                    elif tintero2 == False:
                        tinta_2 = record.oferta_id.attribute_id.cantonera_cliche_id.tinta_2_id.name
                        tintero2 = True
                        if record.oferta_id.attribute_id.cantonera_cliche_id.texto_2:
                            texto_2 = record.oferta_id.attribute_id.cantonera_cliche_id.texto_2
            
            if record.oferta_id.attribute_id.reciclable_id and record.oferta_id.attribute_id.reciclable_id.number > 0:
                if tintero1 == False:
                    texto_1 = record.oferta_id.attribute_id.reciclable_id.name
                elif tintero2 == False:
                    texto_2 = record.oferta_id.attribute_id.reciclable_id.name
            
            
            ala_1 = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_1
            ala_2 = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_2
            grosor = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.grosor_2
            longitud = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud
            
            alas = str(ala_1) + " x " + str(ala_2)
            aux1 = ala_1 - 2
            aux2 = ala_1 + 2
            tolerancia_alas = str(aux1) + " - " + str(aux2) + " x "
            aux1 = ala_2 - 2
            aux2 = ala_2 + 2
            tolerancia_alas = tolerancia_alas + str(aux1) + " - " + str(aux2)
            aux1 = grosor - 0.2
            aux2 = grosor + 0.2
            tolerancia_grosor = str(round(aux1, 2)) + " - " + str(round(aux2, 2))
            aux1 = longitud - 5
            aux2 = longitud + 5
            tolerancia_longitud = str(aux1) + " - " + str(aux2)
            
            ancho_pallet = record.oferta_id.attribute_id.ancho_pallet
            tipo_pallet = ""
            if record.oferta_id.attribute_id.pallet_especial_id:
                tipo_pallet = record.oferta_id.attribute_id.pallet_especial_id.name
            else:
                tipo_pallet = "Pallet de Madera"
            paletizado = "Compacto (Normal)"
            if record.oferta_id.attribute_id.paletizado == 2:
                paletizado = "Columnas" 
            und_paquete = str(record.oferta_id.attribute_id.und_paquete) + " unidades / paquete"
            paquetes_fila = str(record.oferta_id.attribute_id.paquetes_fila) + " paquetes / fila"
            
            und_exactas = ""
            if record.oferta_id.und_exactas == True:
                und_exactas = "SI"
            
            metros = record.und_pallet * record.num_pallets * record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
            peso_interior = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.j_gram / 1000
            peso_interior = peso_interior * record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.j_interior / 1000
            peso_interior = peso_interior * metros * 1.05
            peso_interior = (int(peso_interior / 50) + 1) * 50
            peso_superficie = 0.180 * record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.j_superficie / 1000
            peso_superficie = peso_superficie * metros * 1.05
            peso_superficie = (int(peso_superficie / 50) + 1) * 50
            minutos = int(metros / 60)
            horas = int(minutos / 60)
            minutos = minutos - 60 * horas
            duracion = str(horas) + " horas " + str(minutos) + " minutos"
            metros = str(int(metros)) + " metros"
            peso_interior = str(peso_interior) + " kg"
            peso_superficie = str(peso_superficie) + " kg"
            comentario = ""
            if record.oferta_id.attribute_id.referencia_cliente_id.comentario_paletizado:
                comentario = record.oferta_id.attribute_id.referencia_cliente_id.comentario_paletizado
            
            forma = "Canto Recto"
            if record.oferta_id.attribute_id.cantonera_forma_id:
                forma = record.oferta_id.attribute_id.cantonera_forma_id.name
            
            especial = ""
            if record.oferta_id.attribute_id.cantonera_especial_id:
                especial = record.oferta_id.attribute_id.cantonera_especial_id.name
            
            record.op_cantonera_maquina = maquina
            record.op_superficie_color = superficie_color
            record.op_superficie_ancho = superficie_ancho
            record.op_interior_ancho = interior_ancho
            record.op_interior_gramaje = interior_gramaje
            record.op_tinta_1 = tinta_1
            record.op_texto_1 = texto_1
            record.op_tinta_2 = tinta_2
            record.op_texto_2 = texto_2
            record.op_alas = alas
            record.op_grosor = str(grosor)
            record.op_longitud = str(longitud)
            record.op_tolerancia_alas = tolerancia_alas
            record.op_tolerancia_grosor = tolerancia_grosor
            record.op_tolerancia_longitud = tolerancia_longitud
            record.op_ancho_pallet = str(ancho_pallet)
            record.op_tipo_pallet = tipo_pallet
            record.op_paletizado = paletizado
            record.op_und_paquete = und_paquete
            record.op_paquetes_fila = paquetes_fila
            record.op_und_exactas = und_exactas
            record.op_metros = metros
            record.op_peso_interior = peso_interior
            record.op_peso_superficie = peso_superficie
            record.op_duracion = duracion
            record.op_comentario = comentario
            record.op_forma = forma
            record.op_especial = especial


    
    @api.onchange('oferta_id', 'num_pallets', 'und_user', 'kilos_user', 'importe', 'cantidad', 'precio')
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
                descripcion = record.oferta_id.attribute_id.titulo
            und_pallet = 0
            cantidad = ""
            precio = ""
            importe = 0
            peso_neto = 0
            peso_bruto = 0
            eton = 0

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
                cantidad_num = round(cantidad_num, 4)
                cantidad = str(cantidad_num) + " metros"
                precio_num = record.oferta_id.precio_metro
                precio_num = round(precio_num, 4)
                precio = str(precio_num) + " €/metro"
                if record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro > 0:
                    eton = record.oferta_id.precio_metro * 1000 / record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro
                
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
                cantidad_num = round(cantidad_num, 4)
                cantidad = str(cantidad_num) + " unidades"
                precio_num = record.oferta_id.precio_metro * record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
                precio_num = round(precio_num, 4)
                precio = str(precio_num) + " €/unidad"
                if record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro > 0:
                    eton = record.oferta_id.precio_metro * 1000 / record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro
                
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
                cantidad_num = round(cantidad_num, 4)
                cantidad = str(cantidad_num) + " millares"
                precio_num = record.oferta_id.precio_metro * record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad * 1000
                precio_num = round(precio_num, 4)
                precio = str(precio_num) + " €/millar"
                if record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro > 0:
                    eton = record.oferta_id.precio_metro * 1000 / record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro
                
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
                cantidad_num = round(cantidad_num, 4)
                cantidad = str(cantidad_num) + " kilos"
                precio_num = record.oferta_id.precio_kilo
                precio_num = round(precio_num, 4)
                precio = str(precio_num) + " €/kilo"
                eton = record.oferta_id.precio_kilo * 1000
            #Varios
            elif facturar == '5':
                cantidad_num = record.num_pallets * und_pallet
                cantidad_num = round(cantidad_num, 4)
                cantidad = str(cantidad_num) + " unidades"
                precio_num = record.oferta_id.precio_varios
                precio_num = round(precio_num, 4)
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
    provincia_id = fields.Many2one('res.country.state', string="Provincia")
    transportista = fields.Char('Transportista')
    
    lot_ids = fields.Many2many('stock.production.lot', compute="_get_lots_sale", string="Lotes")

    num_pallets = fields.Integer('Pallets Pedido', compute="_get_num_pallets")
    peso_neto = fields.Integer('Peso Neto', compute="_get_num_pallets")
    peso_bruto = fields.Integer('Peso Bruto', compute="_get_num_pallets")
    eton = fields.Float('Eton', digits=(8, 1), compute="_get_num_pallets")
    importe_sin_descuento = fields.Float('Importe Sin Descuento', digits = (10, 2), compute="_get_num_pallets")
    importe_con_descuento = fields.Float('Importe Total', digits = (10, 2), compute="_get_num_pallets")
    haycodigo = fields.Boolean('Hay Código', compute = "_get_num_pallets")
    
    descuento_euros = fields.Float('Descuento Euros', digits = (10, 2), readonly = True, compute="_get_descuento")
    comercial_bueno_id = fields.Char('Comercial Bueno', compute="_get_descuento")
    no_editar = fields.Boolean('No Editar')
    pedido_stock = fields.Boolean('Pedido de Stock', default = False)
    
    ESTADOS_SEL = [('0', 'NO CONFIRMADO'),     
                  ('1', 'CONFIRMADO'),
                  ('2', 'FABRICADO'),
                  ('3', 'ENTREGA PARCIAL'),
                  ('4', 'ENTREGA TOTAL'),
                  ]
    estado = fields.Selection(selection = ESTADOS_SEL, string = 'Estado pedido', store=True, compute="_get_estado_pedido")
    
    @api.onchange('no_editar',)
    def _onchange_no_editar(self):
        if self.no_editar == True:
            for line in self.order_line:
                line.no_editar = True
                line.attribute_id.write({'no_editar': True})
                line.oferta_id.write({'no_editar': True})
        else:
            for line in self.order_line:
                line.no_editar = False
    
    
    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for so in self:
            so.no_editar = True
            for line in so.order_line:
                line.no_editar = True
                line.attribute_id.no_editar = True
                line.oferta_id.no_editar = True
        return res
        
        

    #@api.depends('importe_con_descuento', 'importe_sin_descuento', 'partner_id.sale_discount')
    def _get_descuento(self):
        for record in self:
            porcentaje = record.partner_id.sale_discount
            euros = record.importe_sin_descuento - record.importe_con_descuento
            record.descuento_euros = euros
            record.comercial_bueno_id = record.partner_id.user_id.id


    
    @api.depends('state', 'invoice_status', 'picking_ids', 'picking_ids.state', 'lot_ids', 'provincia_id')
    def _get_estado_pedido(self):
        for record in self:
            estado = '0'
            if record.state == 'sale' or record.state == 'done':
                estado = '1'
                
                hechos = 0
                totales = 0
                for alb in record.picking_ids:
                    if alb.state == 'done':
                        hechos = hechos + 1
                        totales = totales + 1
                    elif alb.state != 'cancel' and alb.state != 'draft':
                        totales = totales + 1
                        
                if totales > 0:
                    if totales == hechos:
                        estado = '4'
                    elif hechos > 0:
                        estado = '3'
                        
                    elif hechos <= 0:
                        
                        num_lotes = 0
                        
                        if len(record.lot_ids) == record.num_pallets:
                            fabricado = True
                            for lot in record.lot_ids:
                                if lot.fabricado == False:
                                    fabricado = False
                                    break
                            if fabricado == True:
                                estado = '2'
            record.estado = estado
                        
    
    @api.multi
    def create_sale_order_line_referencia(self, line_product_id, lot_ids, referencia_cliente_id, attribute_id, oferta_id, num_pallets):
        for record in self:
        
            if record.no_editar == False:

                product_id = None
                for prod in self.env['product.template'].search([('referencia_id', '=', referencia_cliente_id.referencia_id.id),
                                                                 ]):
                    product_id = prod
     
                if product_id == None:
                    es_vendido = False
                    es_comprado = False
                    tipo_producto = ''
                    cuenta_ingresos_code = -1
                    cuenta_gastos_code = -1
                    
                    if referencia_cliente_id.is_cantonera == True:
                        es_vendido = True
                        es_comprado = False
                        tipo_producto = 'product'
                        cuenta_ingresos_code = 70100001
                        cuenta_gastos_code = -1
                    if referencia_cliente_id.is_perfilu == True:
                        es_vendido = True
                        es_comprado = True
                        tipo_producto = 'product'
                        cuenta_ingresos_code = 70000008
                        cuenta_gastos_code = 60000003
                    if referencia_cliente_id.is_slipsheet == True:
                        es_vendido = True
                        es_comprado = False
                        tipo_producto = 'product'
                        cuenta_ingresos_code = 70100009
                        cuenta_gastos_code = -1
                    if referencia_cliente_id.is_solidboard == True:
                        es_vendido = True
                        es_comprado = False
                        tipo_producto = 'product'
                        cuenta_ingresos_code = 70000011
                        cuenta_gastos_code = -1
                    if referencia_cliente_id.is_formato == True:
                        es_vendido = True
                        es_comprado = True
                        tipo_producto = 'product'
                        cuenta_ingresos_code = 70000004
                        cuenta_gastos_code = 60000004
                    if referencia_cliente_id.is_bobina == True:
                        es_vendido = True
                        es_comprado = True
                        tipo_producto = 'product'
                        cuenta_ingresos_code = 70000004
                        cuenta_gastos_code = 60000004
                    if referencia_cliente_id.is_pieballet == True:
                        es_vendido = True
                        es_comprado = True
                        tipo_producto = 'product'
                        cuenta_ingresos_code = 70000002
                        cuenta_gastos_code = 60000005
                    if referencia_cliente_id.is_flatboard == True:
                        es_vendido = True
                        es_comprado = True
                        tipo_producto = 'product'
                        cuenta_ingresos_code = 70000005
                        cuenta_gastos_code = 60000007
                    if referencia_cliente_id.is_varios == True:
                        es_vendido = True
                        es_comprado = True
                        tipo_producto = 'consu'
                        cuenta_gastos_code = -1
                        if referencia_cliente_id.tipo_varios_id:
                            cuenta_ingresos_code = referencia_cliente_id.tipo_varios_id.number
                    if referencia_cliente_id.is_mprima_papel == True:
                        es_vendido = True
                        es_comprado = False
                        tipo_producto = 'product'
                        cuenta_ingresos_code = 70000004
                        cuenta_gastos_code = 60100001
                    
                    product_id = self.env['product.template'].create({'name': referencia_cliente_id.referencia_id.name, 
                                                                      'type': tipo_producto,
                                                                      'purchase_ok': es_comprado,
                                                                      'sale_ok': es_vendido,
                                                                      'tracking': 'serial',
                                                                      'categ_id': referencia_cliente_id.type_id.id,
                                                                      'referencia_id':referencia_cliente_id.referencia_id.id, 
                                                                      #'property_account_income_id': 
                                                                      #'property_account_expense_id': 
                                                                     })
                
                
                
                discount = 0.0
                if record.general_discount > 0.0:
                    discount = record.general_discount
                if len(lot_ids) > 0 and line_product_id.id == product_id.id:
                
                    sale_line = self.env['sale.order.line'].create({'order_id': record.id, 
                                                        'name':product_id.name, 
                                                        'product_uom_qty': num_pallets,
                                                        'num_pallets': num_pallets,
                                                        'price_unit': oferta_id.cantidad * oferta_id.precio,
                                                        'customer_lead': 1,
                                                        'product_uom': 1,
                                                        'attribute_id': attribute_id.id,
                                                        'oferta_id': oferta_id.id,
                                                        'product_id': product_id.product_variant_id.id,
                                                        'discount': discount,
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
                                                            'customer_lead': 1,
                                                            'product_uom': 1,
                                                            'attribute_id': attribute_id.id,
                                                            'oferta_id': oferta_id.id,
                                                            'product_id': line_product_id.product_variant_id.id,
                                                            'discount': discount,
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
                                                            'customer_lead': 1,
                                                            'product_uom': 1,
                                                            'attribute_id': attribute_id.id,
                                                            'oferta_id': oferta_id.id,
                                                            'product_id': product_id.product_variant_id.id,
                                                            'discount': discount,
                                                           })
                        sale_line._compute_tax_id()
            
            
            
            
            
            
    @api.depends('order_line',)
    def _get_lots_sale(self):
        for record in self:
            record.lot_ids = self.env['stock.production.lot'].search([('sale_order_id', '=', record.id)])

            
            
    @api.depends('order_line.num_pallets', 'order_line.peso_neto', 'order_line.peso_bruto', 'order_line.product_uom_qty', 'order_line.price_unit', 'order_line')
    def _get_num_pallets(self):
    
        for record in self:
            num_pallets = 0
            peso_neto = 0
            peso_bruto = 0
            importe_sin_descuento = 0
            importe_con_descuento = 0
            haycodigo = False
            eton = 0
            
            for line in record.order_line:
                if line.descripcion and len(line.descripcion) > 0 and line.bultos == '1':
                    num_pallets = num_pallets + line.num_pallets
                    peso_neto = peso_neto + (line.peso_neto * line.num_pallets)
                    if line.peso_neto > 0:
                        eton = eton + line.peso_neto * line.num_pallets * line.eton
                    peso_bruto = peso_bruto + (line.peso_bruto * line.num_pallets)
                    importe_sin_descuento = importe_sin_descuento + line.importe
                    importe_con_descuento = importe_con_descuento + line.price_subtotal
                    if line.codigo_cliente and len(line.codigo_cliente) > 0:
                        haycodigo = True
            
            if peso_neto > 0:
                eton = eton / peso_neto
            record.num_pallets = num_pallets
            record.peso_neto = peso_neto
            record.peso_bruto = peso_bruto
            record.importe_sin_descuento = importe_sin_descuento
            record.importe_con_descuento = importe_con_descuento
            record.haycodigo = haycodigo
            record.eton = eton


    
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
                cliente_id = record.partner_id.id
                if record.pedido_stock == True:
                    cliente_id = None
            
                if line.bultos == '1':
                    cantidad_a_fabricar = int(line.product_uom_qty) - len(line.lot_ids)

                    if cantidad_a_fabricar > 0:
                        i = 0
                        while i < cantidad_a_fabricar:
                            i = i+1
                    
                            if line.product_id:
                                #Creamos lotes
                                lot_id = self.env['stock.production.lot'].create({'product_id': line.product_id.id, 
                                                            'name': self.env['ir.sequence'].next_by_code('stock.lot.serial'), 
                                                            'referencia_id': line.product_id.referencia_id.id, 
                                                            'cliente_id': cliente_id,
                                                            'sale_order_line_id': line.id,
                                                            'fabricado': False,
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
