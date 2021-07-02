from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)
from odoo import exceptions
import requests

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    id_producto = fields.Integer("ID Producto", readonly = True, compute = "_get_id")
    id_referencia = fields.Integer("ID Referencia", readonly = True, compute = "_get_id")

    lot_ids = fields.One2many('stock.production.lot', 'sale_order_line_id', string="Lotes", )
    
    fila_vinculada_id = fields.Many2one('sale.order.line', string="Unidades Vinculadas")
    und_lotes = fields.Integer('Unidades Lotes', readonly = True, compute = "_get_und_lotes")
    
    attribute_id = fields.Many2one('sale.product.attribute', string="Atributo producto", )
    oferta_id = fields.Many2one('sale.offer.oferta', string="Oferta")
    und_user = fields.Integer('Und Pallet Fabricadas', default = -1)
    kilos_user = fields.Float('kg Pallet Fabricados', digits=(10, 2), default = -1)
    num_pallets = fields.Integer('Num Pallets', default = 1)
    BULTOS_SEL = [('1', 'SI'),     
                  ('2', 'NO'),
                  ]
    bultos = fields.Selection(selection = BULTOS_SEL, string = 'Es pallet', default='1')
    aclaracion = fields.Char('Aclaración')
    hayaclaracion = fields.Boolean('Hay Aclaración', compute = "_hay_aclaracion")
    no_editar = fields.Boolean('No Editar')
    
    superorden_id = fields.Many2one('stock.production.superorden', string="Superorden")
    
    #Campos calculados
    codigo_cliente = fields.Char('Código cliente', readonly = True, compute = "_get_valores")
    descripcion = fields.Html('Descripción', readonly = True, compute = "_get_valores")
    und_pallet = fields.Integer('Unidades Pallet', readonly = True, compute = "_get_valores")
    cantidad = fields.Char('Cantidad', compute = "_get_valores")
    precio = fields.Char('Precio', readonly = True, compute = "_get_valores")
    cantidad_num_1 = fields.Float('Cantidad Num 1', readonly = True, compute = "_get_valores")
    precio_num = fields.Float('Precio Num', readonly = True, compute = "_get_valores")
    importe = fields.Float('Importe', digits = (10,2), readonly = True, compute = "_get_valores")
    peso_neto = fields.Integer('Peso Neto Pallet', readonly = True, compute = "_get_valores")
    peso_bruto = fields.Integer('Peso Bruto Pallet', readonly = True, compute = "_get_valores")
    eton = fields.Float('Eton', digits=(8, 1), readonly = True, compute = "_get_valores")
    facturar = fields.Char('Facturar Por', readonly = True, compute = "_get_valores")
    
    orden_fabricacion = fields.Char('Orden Fabricación', compute = "_get_produccion")
    lotes_fabricar = fields.Integer('Lotes Fabricar', default = 1)
    lotes_inicio = fields.Integer('Lotes Inicio', default = 1)
    actualizar = fields.Boolean('Actualizar')
    dir_qr = fields.Char('Dir QR Lote', readonly = True, compute = "_get_produccion")
    dir_qr_orden = fields.Char('Dir QR Orden', readonly = True, compute = "_get_produccion")
    incompleta = fields.Boolean('Incompleta', readonly = True, store = True, compute = "_get_und_lotes")
    
    
    ESTADO_SEL = [('0', 'NO FABRICAR'),    
                  ('1', 'FABRICAR'),
                  ('3', 'FABRICADO STOCK'),
                  ]
    estado_linea = fields.Selection(selection = ESTADO_SEL, string = 'Estado', default = '1')
    
    op_cantonera_maquina = fields.Char('Máquina', compute = "_get_produccion")
    op_superficie_color = fields.Char('Superficie Color', compute = "_get_produccion")
    op_superficie_ancho = fields.Char('Superficie Ancho', compute = "_get_produccion")
    op_interior_ancho = fields.Char('Interior Ancho', compute = "_get_produccion")
    op_interior_gramaje = fields.Char('Interior Gramaje', compute = "_get_produccion")
    op_rodillo = fields.Char('Rodillo', compute = "_get_produccion")
    op_tinta_1 = fields.Char('Tinta 1', compute = "_get_produccion")
    op_texto_1 = fields.Char('Texto 1', compute = "_get_produccion")
    op_tinta_2 = fields.Char('Tinta 2', compute = "_get_produccion")
    op_texto_2 = fields.Char('Texto 2', compute = "_get_produccion")
    op_alas = fields.Char('Alas', compute = "_get_produccion")
    op_grosor = fields.Char('Grosor', compute = "_get_produccion")
    op_longitud = fields.Char('Longitud', compute = "_get_produccion")
    op_hendido = fields.Char('Hendido', compute = "_get_produccion")
    op_und_pallet = fields.Integer('Und Orden', compute = "_get_produccion")
    op_num_pallets = fields.Integer('Num Pallets', compute = "_get_produccion")
    op_sierra = fields.Html('Sierra', compute = "_get_produccion", store=True)
    op_tolerancia_alas = fields.Char('Tolerancia Alas', compute = "_get_produccion")
    op_tolerancia_grosor = fields.Char('Tolerancia Grosor', compute = "_get_produccion")
    op_tolerancia_longitud = fields.Char('Tolerancia Longitud', compute = "_get_produccion")
    op_ancho_pallet = fields.Char('Ancho Pallet', compute = "_get_produccion")  
    op_tipo_pallet = fields.Char('Tipo Pallet', compute = "_get_produccion")
    op_paletizado = fields.Char('Paletizado', compute = "_get_produccion")
    op_und_paquete = fields.Integer('Unidades Paquete', compute = "_get_produccion")
    op_paquetes_fila= fields.Integer('Paquetes Fila', compute = "_get_produccion")
    op_und_exactas = fields.Char('Unidades Exactas', compute = "_get_produccion")
    op_metros = fields.Char('Metros', compute = "_get_produccion")
    op_metros_num = fields.Integer('Metros', compute = "_get_produccion")
    op_peso_interior = fields.Char('Peso Interior', compute = "_get_produccion")
    op_peso_superficie = fields.Char('Peso Superficie', compute = "_get_produccion")
    op_velocidad = fields.Integer('Velocidad', compute = "_get_produccion")
    op_comentario = fields.Char('Comentario', compute = "_get_produccion")
    op_forma = fields.Char('Forma', compute = "_get_produccion")
    op_especial = fields.Char('Especial', compute = "_get_produccion")
    op_tipo_papel = fields.Char('Tipo Papel', compute = "_get_produccion")
    op_demanda = fields.Html('Demanda Papel', compute = "_get_produccion")
    
    ESTADO_PRODUC_CANTONERA = [('0', 'SIN ASIGNAR'),    
                               ('1', 'LÍNEA 1'),
                               ('2', 'LÍNEA 2'),
                               ('3', 'LÍNEA 3'),
                               ('4', 'LÍNEA 4'),
                               ]
    estado_cantonera = fields.Selection(selection = ESTADO_PRODUC_CANTONERA, string = 'Estado Cantonera', default = '0', group_expand='_read_estado_cantonera')
    
    ESTADO_PRODUC_SLIPSHEET = [('10', '10'),    
                               ('11', '11'),
                               ('12', '12'),
                               ]
    estado_slipsheet = fields.Selection(selection = ESTADO_PRODUC_SLIPSHEET, string = 'Estado Slipsheet', default = '10', group_expand='_read_estado_slipsheet')
    
    ESTADO_SIERRA = [('0', '0'),    
                       ('1', '1'),
                       ('2', '2'),
                       ]
    estado_sierra = fields.Selection(selection = ESTADO_SIERRA, string = 'Estado Sierra', default = '0', group_expand='_read_estado_sierra')
    
    sequence_cantonera = fields.Integer('Secuencia kanban', default=50)
    color = fields.Integer('Color')
    
    horas = fields.Float('Horas', digits = (8, 1), compute = "_get_horas", store=True)
    op_duracion = fields.Char('Duración', compute = "_get_horas")
    cliente_nombre = fields.Char('Cliente', compute = "_get_horas")
    fecha_entrega = fields.Char('Fecha entrega', compute = "_get_horas")
    
    fsc_linea = fields.Char('FSC Línea', compute = "_get_fsc")
    fsc_valido = fields.Boolean('FSC Válido', compute = "_get_fsc")
    fsc_venta = fields.Boolean('FSC Venta', default = False)
    
    kanban_state = fields.Selection([
        ('normal', 'Grey'),
        ('done', 'Green'),
        ('blocked', 'Red')], string='Kanban State',
        copy=False, default='normal')
        
        
    
    @api.onchange('estado_cantonera',)
    def _onchange_estado_produccion(self):
        self.sequence_cantonera = 999
        i = self.ordenar_secuencia_cantonera(self.estado_cantonera)
        self.sequence_cantonera = i
        

            
    def ordenar_secuencia_cantonera(self, estado_cantonera):
        i=1
        for line in self.env['sale.order.line'].search([('product_id.categ_id.is_cantonera', '=', True), 
                                                        ('incompleta', '=', True), 
                                                        ('estado_cantonera', '=', estado_cantonera)], 
                                                        order='sequence_cantonera'):
            line.write({'sequence_cantonera': i})
            i = i+1
        return i
    
        
        
        
    
    @api.depends('estado_cantonera', 'estado_slipsheet', 'op_velocidad', 'oferta_id')
    def _get_horas(self):
        for record in self:
            velocidad = record.op_velocidad
            minutos = 0
            horas = 0
            duracion = ""
            if record.product_id.categ_id.is_cantonera == True:
                if record.estado_cantonera == '0':
                    minutos = int(record.op_metros_num / velocidad)
                    horas = minutos / 60
                elif record.estado_cantonera == '1' and record.oferta_id.attribute_id.cantonera_1 == True:
                    velocidad = velocidad / 2
                    minutos = int(record.op_metros_num / velocidad)
                    horas = minutos / 60
                elif record.estado_cantonera == '2' and record.oferta_id.attribute_id.cantonera_2 == True:
                    minutos = int(record.op_metros_num / velocidad)
                    horas = minutos / 60
                elif record.estado_cantonera == '3' and record.oferta_id.attribute_id.cantonera_3 == True:
                    minutos = int(record.op_metros_num / velocidad)
                    horas = minutos / 60
                elif record.estado_cantonera == '4' and record.oferta_id.attribute_id.cantonera_4 == True:
                    minutos = int(record.op_metros_num / velocidad)
                    horas = minutos / 60
                
                if minutos > 0:
                    horas_dur = int(horas)
                    minutos = minutos - horas_dur * 60
                    duracion = str(horas_dur) + " horas y " + str(minutos) + " minutos"
                else:
                    duracion = "LÍNEA INCORRECTA"
                
            elif record.product_id.categ_id.is_slipsheet == True:
                if record.estado_slipsheet == '10':
                    minutos = 6
                elif record.estado_slipsheet == '11':
                    minutos = 7
                elif record.estado_slipsheet == '12':
                    minutos = 8
            
            cliente_nombre = ""
            fecha_entrega = None
            if record.order_id:
                if record.order_id.partner_id:
                    cliente_nombre = record.order_id.partner_id.name
                if record.order_id.fecha_entrega:
                    fecha_entrega = record.order_id.fecha_entrega
                
            record.cliente_nombre = cliente_nombre
            record.fecha_entrega = fecha_entrega
            record.horas = horas
            record.op_duracion = duracion
    
    
    @api.model
    def _read_estado_cantonera(self, stages, domain, order):
        return ['0','1','2','3','4',]
        
    @api.model
    def _read_estado_slipsheet(self, stages, domain, order):
        return ['10','11','12',]
        
    @api.model
    def _read_estado_sierra(self, stages, domain, order):
        return ['0','1','2',]
        
    
    
    @api.multi
    def action_decrease_sequence(self):
        for record in self:
            record.ordenar_secuencia_cantonera(record.estado_cantonera)
            if record.sequence_cantonera > 1:
                new_sequence = record.sequence_cantonera - 1
                for line in self.env['sale.order.line'].search([('product_id.categ_id.is_cantonera', '=', True), 
                                                        ('incompleta', '=', True), 
                                                        ('estado_cantonera', '=', self.estado_cantonera),
                                                        ('sequence_cantonera', '=', new_sequence)]):
                    line.sequence_cantonera = new_sequence + 1
                record.sequence_cantonera = new_sequence
                
            return {
                  'type': 'ir.actions.client',
                  'tag': 'reload',
            }
            
    @api.multi
    def action_increase_sequence(self):
        for record in self:
            record.ordenar_secuencia_cantonera(record.estado_cantonera)
            if len(self.env['sale.order.line'].search([('product_id.categ_id.is_cantonera', '=', True), 
                                                        ('incompleta', '=', True), 
                                                        ('estado_cantonera', '=', self.estado_cantonera),
                                                        ('sequence_cantonera', '>', record.sequence_cantonera)])) > 0:
                
                
                new_sequence = record.sequence_cantonera + 1
                for line in self.env['sale.order.line'].search([('product_id.categ_id.is_cantonera', '=', True), 
                                                        ('incompleta', '=', True), 
                                                        ('estado_cantonera', '=', self.estado_cantonera),
                                                        ('sequence_cantonera', '=', new_sequence)]):
                    line.sequence_cantonera = new_sequence + -1
                record.sequence_cantonera = new_sequence
        
        

            return {
                  'type': 'ir.actions.client',
                  'tag': 'reload',
            }
    
    
    
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
    
    @api.depends('product_id', 'oferta_id')
    def _get_fsc(self):
        for record in self:
            fsc_linea = ""
            fsc_valido = True
            #Comprobamos todos los lotes de la linea y el tipo de fsc
            for lote in record.lot_ids:
                if fsc_linea == "":
                    fsc_linea = lote.fsc_nombre
                elif fsc_linea == "FSC Ninguno":
                    fsc_linea = "FSC Ninguno"
                elif lote.fsc_nombre == "FSC Ninguno":
                    fsc_linea = "FSC Ninguno"
                elif lote.fsc_nombre == fsc_linea:
                    fsc_linea = lote.fsc_nombre
                else:
                    fsc_linea = "FSC Desconocido"
            
            if fsc_linea == "FSC Ninguno":
                fsc_valido = False
            elif fsc_linea == "FSC Desconocido":
                fsc_valido = False
            
            record.fsc_linea = fsc_linea
            record.fsc_valido = fsc_valido
    
    
    @api.depends('product_id', 'oferta_id')
    def _get_id(self):
        for record in self:
            id_producto = 0
            id_referencia = 0
            
            if record.product_id:
                id_producto = record.product_id.id
            if record.oferta_id:
                id_referencia = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.id
                
            record.id_producto = id_producto
            record.id_referencia = id_referencia

            
    
    @api.depends('lot_ids', 'num_pallets', 'estado_linea')
    def _get_und_lotes(self):
        for record in self:
            unidades = 0
            for lot in record.lot_ids:
                unidades = unidades + lot.unidades
            
            incompleta = False
            if len(record.lot_ids) < record.num_pallets:
                incompleta = True
                #No fabricar
                if record.estado_linea == '0':
                    incompleta = False
                #Fabricado Stock
                if record.estado_linea == '3':
                    incompleta = False
                
            record.und_lotes = unidades
            record.incompleta = incompleta
    
    
    
    @api.onchange('lot_ids',)
    def _onchange_lot_ids(self):
        for lot in self.lot_ids:
            lot.descripcion = self.descripcion
        
    
    
    @api.onchange('no_editar',)
    def _onchange_no_editar(self):
        if self.no_editar == True:
            self.attribute_id.write({'no_editar': True})
            self.oferta_id.write({'no_editar': True})
    
    

    @api.onchange('lot_ids', 'num_pallets')
    def _onchange_lotes_fabricar(self):
        self.lotes_fabricar = self.num_pallets - len(self.lot_ids)

    
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
            
           
    
    @api.depends('oferta_id', 'und_pallet', 'num_pallets', 'lotes_inicio', 'lotes_fabricar')
    def _get_produccion(self):
        for record in self:
            
            op_tipo_papel = "ORDEN NORMAL - Papel Normal, Mixto o Reciclado"
            op_fsc = 0
            if record.oferta_id.attribute_id.fsc_id:
                op_fsc = record.oferta_id.attribute_id.fsc_id.number
                if record.oferta_id.attribute_id.fsc_id.number == 1:
                    op_tipo_papel = "ORDEN FSC - Papel Mixto o Reciclado"
                elif record.oferta_id.attribute_id.fsc_id.number == 2:
                    op_tipo_papel = "ORDEN MIXTO - Papel Mixto"
                elif record.oferta_id.attribute_id.fsc_id.number == 3:
                    op_tipo_papel = "ORDEN RECICLADO - Papel Reciclado"
            record.op_tipo_papel = op_tipo_papel
            
            orden_fabricacion = str(record.order_id.id) + "-" + str(record.id)
            dir_qr = "http://bemecopack.es/jseb/qr_lote.php?orden="
            dir_qr = dir_qr + orden_fabricacion
            record.dir_qr = dir_qr
            record.orden_fabricacion = orden_fabricacion

            maquina = ""
            if record.oferta_id.attribute_id.is_cantonera == True:
                if record.oferta_id.attribute_id.cantonera_1 == True:
                    maquina = maquina + "Línea 1, "
                if record.oferta_id.attribute_id.cantonera_2 == True:
                    maquina = maquina + "Línea 2, "
                if record.oferta_id.attribute_id.cantonera_3 == True:
                    maquina = maquina + "Línea 3, "
                if record.oferta_id.attribute_id.cantonera_4 == True:
                    maquina = maquina + "Línea 4, "
            elif record.oferta_id.attribute_id.is_slipsheet == True:
                maquina = "Contracoladora 1"
            elif record.oferta_id.attribute_id.is_solidboard == True:
                maquina = "Contracoladora 1"
            
            superficie_color = ""
            if record.oferta_id.attribute_id.cantonera_color_id:
                superficie_color = record.oferta_id.attribute_id.cantonera_color_id.name
                
            superficie_ancho = "" 
            interior_ancho = ""
            interior_gramaje = ""

            if record.oferta_id.attribute_id.is_cantonera == True:
                if record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ancho_superficie:
                    superficie_ancho = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ancho_superficie
                if record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ancho_interior:
                    interior_ancho = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ancho_interior 
                
                aux2 = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.j_gram + 100
                interior_gramaje = str(record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.j_gram) + " - " + str(aux2)
                    
            elif record.oferta_id.attribute_id.is_slipsheet == True:
                interior_ancho = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ancho
                interior_ancho = interior_ancho + record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_1
                interior_ancho = interior_ancho + record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_2 
                superficie_ancho = interior_ancho + 30

                interior_gramaje = record.oferta_id.attribute_id.gramaje
                
            elif record.oferta_id.attribute_id.is_solidboard == True:
                interior_ancho = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ancho
                interior_ancho = interior_ancho + record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_1
                interior_ancho = interior_ancho + record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_2
                superficie_ancho = interior_ancho + 30
                
                interior_gramaje = record.oferta_id.attribute_id.gramaje
            
            ala_1 = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_1
            ala_2 = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_2
            
            grosor = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.grosor_2
            if record.oferta_id.attribute_id.is_slipsheet == True:
                grosor = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.grosor_1
            elif record.oferta_id.attribute_id.is_solidboard == True:
                grosor = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.grosor_1
                
            longitud_final = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud
            longitud = longitud_final
            und_pallet = record.und_pallet
            num_pallets = record.lotes_fabricar
            sierra = ""
            
            velocidad = 60
            
            rodillo = ""
            tintero1 = False
            tintero2 = False
            tinta_1 = ""
            texto_1 = ""
            tinta_2 = ""
            texto_2 = ""
            if record.oferta_id.attribute_id.cantonera_cliche_id:
                rodillo = record.oferta_id.attribute_id.cantonera_cliche_id.rodillo
                if record.oferta_id.attribute_id.cantonera_cliche_id.tinta_1_id:
                    tinta_1 = record.oferta_id.attribute_id.cantonera_cliche_id.tinta_1_id.name
                    tintero1 = True
                    velocidad = velocidad - 10
                    if record.oferta_id.attribute_id.cantonera_cliche_id.texto_1:
                        texto_1 = record.oferta_id.attribute_id.cantonera_cliche_id.texto_1
                if record.oferta_id.attribute_id.cantonera_cliche_id.tinta_2_id:
                    if tintero1 == False:
                        tinta_1 = record.oferta_id.attribute_id.cantonera_cliche_id.tinta_2_id.name
                        tintero1 = True
                        velocidad = velocidad - 10
                        if record.oferta_id.attribute_id.cantonera_cliche_id.texto_2:
                            texto_1 = record.oferta_id.attribute_id.cantonera_cliche_id.texto_2
                    elif tintero2 == False:
                        tinta_2 = record.oferta_id.attribute_id.cantonera_cliche_id.tinta_2_id.name
                        tintero2 = True
                        velocidad = velocidad - 10
                        if record.oferta_id.attribute_id.cantonera_cliche_id.texto_2:
                            texto_2 = record.oferta_id.attribute_id.cantonera_cliche_id.texto_2
            
            if record.oferta_id.attribute_id.reciclable_id and record.oferta_id.attribute_id.reciclable_id.number > 0:
                if rodillo == "":
                    if longitud_final >= 800:
                        rodillo = "400 o 750"
                    elif longitud_final >= 400:
                        rodillo = "400"
                    else:
                        rodillo = "400 o 750"
                    
                if tintero1 == False:
                    texto_1 = record.oferta_id.attribute_id.reciclable_id.name
                    rodillo_1 = rodillo
                elif tintero2 == False:
                    texto_2 = record.oferta_id.attribute_id.reciclable_id.name
                    rodillo_2 = rodillo
            
            ancho_pallet = record.oferta_id.attribute_id.ancho_pallet
            tipo_pallet = ""
            if record.oferta_id.attribute_id.pallet_especial_id:
                tipo_pallet = record.oferta_id.attribute_id.pallet_especial_id.name
            else:
                tipo_pallet = "Pallet de Madera"
            paletizado = "Compacto (Normal)"
            if record.oferta_id.attribute_id.paletizado == 2:
                paletizado = "4 Columnas" 
            elif record.oferta_id.attribute_id.paletizado == 3:
                paletizado = '2 Columnas'
            #und_paquete = str(record.oferta_id.attribute_id.und_paquete) + " unidades / paquete"
            #paquetes_fila = str(record.oferta_id.attribute_id.paquetes_fila) + " paquetes / fila"
            und_paquete = record.oferta_id.attribute_id.und_paquete
            paquetes_fila = record.oferta_id.attribute_id.paquetes_fila
            
            und_exactas = ""
            if record.oferta_id.und_exactas == True:
                und_exactas = "SI"
                
            peso_unidad = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro * longitud_final / 1000
            
            if record.oferta_id.attribute_id.sierra == True:
                num_cortes = int(2400 / longitud_final)
                longitud = (longitud_final + 5) * num_cortes + 100
                pesoSierra = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro * longitud / 1000 * record.oferta_id.attribute_id.und_paquete
                while longitud > 2400 or pesoSierra > 15:
                    num_cortes = num_cortes - 1
                    longitud = (longitud_final + 5) * num_cortes + 100
                    pesoSierra = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro * longitud / 1000 * record.oferta_id.attribute_id.und_paquete
                if num_cortes > 0 and record.oferta_id.attribute_id.und_paquete > 0:
                    und_pallet = int(record.und_pallet * record.num_pallets / num_cortes / record.oferta_id.attribute_id.und_paquete) * record.oferta_id.attribute_id.und_paquete
                while record.und_pallet > und_pallet * num_cortes:
                    und_pallet = und_pallet + record.oferta_id.attribute_id.und_paquete
                #und_pallet = und_pallet + record.oferta_id.attribute_id.und_paquete
                
                peso_unidad = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro * longitud / 1000
                num_pallets = 1
                peso_pallet = und_pallet * peso_unidad
                while peso_pallet > 1500:
                    num_pallets = num_pallets + 1
                    if num_pallets > 0:
                        peso_pallet = und_pallet * peso_unidad / num_pallets
                    
                if num_pallets > 0 and record.oferta_id.attribute_id.und_paquete > 0:
                    und_pallet = int(und_pallet / num_pallets / record.oferta_id.attribute_id.und_paquete) * record.oferta_id.attribute_id.und_paquete
                und_pallet = und_pallet + record.oferta_id.attribute_id.und_paquete
                
                p2 = longitud_final * num_cortes + 300
                p3 = 3300 + longitud_final
                sierra = "Parámetro_1: " + str(longitud_final) + "   -   Parámetro_2: " + str(p2) + "   -   R_120: " + str(p3) + "<br/>"
                if longitud_final >= 200:
                    sierra = sierra + str(paquetes_fila) + " paquetes/fila   -   " + str(record.und_pallet) + " unidades / pallet" + "   -   " + str(record.num_pallets) + " pallets"
                else:
                    und_total_sacos = record.und_pallet * record.num_pallets
                    sierra = sierra + "Paletizado en Cajas o Sacos - Total " + str(und_total_sacos) + " unidades"
                paquetes_fila = 0
                und_exactas = "SI"
            
            tolerancia_alas = ""
            tolerancia_grosor = ""
            tolerancia_longitud = ""
            alas = ""
            hendido = "NO"
            
            if record.oferta_id.attribute_id.is_cantonera == True:
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
            
            elif record.oferta_id.attribute_id.is_slipsheet == True:
                aux1 = interior_ancho - 7
                aux2 = interior_ancho + 7
                tolerancia_alas = str(aux1) + " - " + str(aux2)
                
                longitud = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud
                longitud = longitud + record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_3
                longitud = longitud + record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_4 
                
                aux1 = longitud - 7
                aux2 = longitud + 7
                tolerancia_longitud = str(aux1) + " - " + str(aux2)
                
                aux1 = grosor - 0.1
                aux2 = grosor + 0.1
                tolerancia_grosor = str(round(aux1, 2)) + " - " + str(round(aux2, 2))
                
                if record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_1 > 0:
                    hendido = str(record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_1) + " mm"
                if record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_2 > 0:
                    if hendido == "NO":
                        hendido = str(record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_2) + " mm"
                    else:
                        hendido = hendido + " y " + str(record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_2) + " mm"
                
            elif record.oferta_id.attribute_id.is_solidboard == True:
                aux1 = interior_ancho - 7
                aux2 = interior_ancho + 7
                tolerancia_alas = str(aux1) + " - " + str(aux2)
                
                longitud = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud
                longitud = longitud + record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_3
                longitud = longitud + record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_4 
                
                aux1 = longitud - 7
                aux2 = longitud + 7
                tolerancia_longitud = str(aux1) + " - " + str(aux2)

                if record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_1 > 0:
                    hendido = str(record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_1) + " mm"
                if record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_2 > 0:
                    if hendido == "NO":
                        hendido = str(record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_2) + " mm"
                    else:
                        hendido = hendido + " y " + str(record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_2) + " mm"

                    
            metros = und_pallet * num_pallets * longitud / 1000
            peso_interior = record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.j_gram / 1000
            peso_interior = peso_interior * record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.j_interior / 1000
            peso_interior = peso_interior * metros * 1.05
            peso_interior = (int(peso_interior / 50) + 1) * 50
            peso_superficie = 0.180 * record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.j_superficie / 1000
            peso_superficie = peso_superficie * metros * 1.05
            peso_superficie = (int(peso_superficie / 50) + 1) * 50
            metros_num = metros
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
                velocidad = velocidad - 20

            dir_qr_orden = "http://bemecopack.es/jseb/qr_orden.php?"
            
            if record.oferta_id and record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.is_cantonera == True:
                dir_qr_orden = dir_qr_orden + "orden=" + orden_fabricacion
                dir_qr_orden = dir_qr_orden + "&prod=1"
                dir_qr_orden = dir_qr_orden + "&ala1=" + str(ala_1)
                dir_qr_orden = dir_qr_orden + "&ala2=" + str(ala_2)
                dir_qr_orden = dir_qr_orden + "&gros=" + str(grosor)
                dir_qr_orden = dir_qr_orden + "&long1=" + str(longitud)
                dir_qr_orden = dir_qr_orden + "&peso=" + str(round(record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro, 4))
                dir_qr_orden = dir_qr_orden + "&long2=" + str(longitud_final)
                dir_qr_orden = dir_qr_orden + "&fsc=" + str(op_fsc)
                dir_qr_orden = dir_qr_orden + "&palini=" + str(record.lotes_inicio)
                dir_qr_orden = dir_qr_orden + "&npal=" + str(num_pallets)
                dir_qr_orden = dir_qr_orden + "&npalm=" + str(record.lotes_fabricar)
                
            elif record.oferta_id.attribute_id.is_slipsheet == True:                 
                dir_qr_orden = dir_qr_orden + "orden=" + orden_fabricacion
                dir_qr_orden = dir_qr_orden + "&prod=3"
                dir_qr_orden = dir_qr_orden + "&ala1=" + str(ala_1)
                dir_qr_orden = dir_qr_orden + "&ancho=" + str(record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ancho)
                dir_qr_orden = dir_qr_orden + "&ala2=" + str(ala_2)
                dir_qr_orden = dir_qr_orden + "&ala3=" + str(record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_3)
                dir_qr_orden = dir_qr_orden + "&long1=" + str(longitud)
                dir_qr_orden = dir_qr_orden + "&ala4=" + str(record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_4)
                dir_qr_orden = dir_qr_orden + "&gros=" + str(grosor)
                dir_qr_orden = dir_qr_orden + "&peso=" + str(round(record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro, 4))
                dir_qr_orden = dir_qr_orden + "&fsc=" + str(op_fsc)
                dir_qr_orden = dir_qr_orden + "&palini=" + str(record.lotes_inicio)
                dir_qr_orden = dir_qr_orden + "&npal=" + str(num_pallets)
                
            elif record.oferta_id.attribute_id.is_solidboard == True:
                dir_qr_orden = dir_qr_orden + "orden=" + orden_fabricacion
                dir_qr_orden = dir_qr_orden + "&prod=4"
                dir_qr_orden = dir_qr_orden + "&ancho=" + str(record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ancho)
                dir_qr_orden = dir_qr_orden + "&long1=" + str(longitud)
                dir_qr_orden = dir_qr_orden + "&gros=" + str(grosor)
                dir_qr_orden = dir_qr_orden + "&peso=" + str(round(record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro, 4))
                dir_qr_orden = dir_qr_orden + "&fsc=" + str(op_fsc)
                dir_qr_orden = dir_qr_orden + "&palini=" + str(record.lotes_inicio)
                dir_qr_orden = dir_qr_orden + "&npal=" + str(num_pallets)
            
            record.dir_qr_orden = dir_qr_orden
            
            demanda = "http://bemecopack.es/jseb/pedido.php?"
            demanda = demanda + "nombre=" + orden_fabricacion

            if record.oferta_id and record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.is_cantonera == True:
                demanda = demanda + "&producto=1"
                demanda = demanda + "&ala1=" + str(ala_1)
                demanda = demanda + "&ala2=" + str(ala_2)
                demanda = demanda + "&grosor=" + str(grosor)
                demanda = demanda + "&longitud=" + str(longitud)
                metros_pallet = und_pallet * longitud / 1000 * record.lotes_fabricar
                if record.estado_linea != '1':
                    metros_pallet = 0
                if record.lotes_fabricar == 0:
                    metros_pallet = 0
                demanda = demanda + "&metros=" + str(metros_pallet)
                color_demanda = record.oferta_id.attribute_id.cantonera_color_id.id
                demanda = demanda + "&color=" + str(color_demanda)
                demanda = demanda + "&fsc=" + str(op_fsc)
                fecha_entrega = "3000-12-31"
                if record.order_id.fecha_entrega:
                    fecha_entrega = record.order_id.fecha_entrega
                elif record.order_id.fecha_entrega_cliente:
                    fecha_entrega = record.order_id.fecha_entrega_cliente
                demanda = demanda + "&entrega=" + str(fecha_entrega)
                demanda = demanda + "&inicio=" + str(record.lotes_inicio)
                
                if record.oferta_id.attribute_id.referencia_cliente_id.jose == True:
                    demanda = demanda + "&jose=1"
                else:
                    demanda = demanda + "&jose=0"
            
            op_demanda = ""
            try:
                respuesta = requests.get(demanda)
                op_demanda = respuesta.text
            except:
                op_demanda = ""
        
            record.op_demanda = op_demanda
            
            record.op_hendido = hendido
            record.op_cantonera_maquina = maquina
            record.op_superficie_color = superficie_color
            record.op_superficie_ancho = superficie_ancho
            record.op_interior_ancho = interior_ancho
            record.op_interior_gramaje = interior_gramaje
            record.op_rodillo = rodillo
            record.op_tinta_1 = tinta_1
            record.op_texto_1 = texto_1
            record.op_tinta_2 = tinta_2
            record.op_texto_2 = texto_2
            record.op_alas = alas
            record.op_grosor = str(grosor)
            record.op_longitud = str(longitud)
            record.op_sierra = sierra
            record.op_tolerancia_alas = tolerancia_alas
            record.op_tolerancia_grosor = tolerancia_grosor
            record.op_tolerancia_longitud = tolerancia_longitud
            record.op_ancho_pallet = str(ancho_pallet)
            record.op_tipo_pallet = tipo_pallet
            record.op_paletizado = paletizado
            record.op_und_paquete = und_paquete
            record.op_und_pallet = und_pallet
            record.op_num_pallets = num_pallets
            record.op_paquetes_fila = paquetes_fila
            record.op_und_exactas = und_exactas
            record.op_metros = metros
            record.op_metros_num = metros_num
            record.op_peso_interior = peso_interior
            record.op_peso_superficie = peso_superficie
            record.op_velocidad = velocidad
            record.op_comentario = comentario
            record.op_forma = forma
            record.op_especial = especial


    
    @api.onchange('num_pallets', 'importe')
    def _onchange_oferta_cantidad(self):
        if self.actualizar == True:
            self.actualizar = False
        else:
            self.actualizar = True
        
        if self.order_id.actualizar == True:
            self.order_id.actualizar = False
        else:
            self.order_id.actualizar = True
    
    
    
    @api.depends('oferta_id', 'num_pallets', 'und_user')
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
            facturar = record.oferta_id.attribute_id.referencia_cliente_id.precio_cliente
            cantidad_num = 0
            cantidad_num_1 = 0
            precio_num = 0

            if record.und_user > 0:
                und_pallet = record.und_user
            elif record.fila_vinculada_id:
                if record.oferta_id.attribute_id.contar_pallet == True:
                    longitud = record.fila_vinculada_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud
                    pallets = int(longitud / 800)
                    if pallets == 0:
                        pallets = 1
                        
                    und_pallet = pallets * record.fila_vinculada_id.num_pallets
                
                elif len(record.fila_vinculada_id.lot_ids) < record.fila_vinculada_id.num_pallets:
                    #und_pallet = record.fila_vinculada_id.und_pallet * record.fila_vinculada_id.num_pallets
                    if record.fila_vinculada_id.oferta_id:
                        und_pallet = record.fila_vinculada_id.oferta_id.unidades * record.fila_vinculada_id.num_pallets
                else:
                    und_pallet = record.fila_vinculada_id.und_lotes
            else:
                und_pallet = record.oferta_id.unidades
           
            #metros
            if facturar == '1':
                cantidad_num_1 = und_pallet * record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
                cantidad_num = record.num_pallets * und_pallet * record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
                cantidad_num = round(cantidad_num, 4)
                cantidad = str(cantidad_num) + " metros"
                precio_num = record.oferta_id.precio_metro
                precio_num = round(precio_num, 4)
                precio = str(precio_num) + " €/metro"
                if record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro > 0:
                    eton = record.oferta_id.precio_metro * 1000 / record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro
                
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
                cantidad_num_1 = und_pallet
                cantidad_num = record.num_pallets * und_pallet
                cantidad_num = round(cantidad_num, 4)
                cantidad = str(cantidad_num) + " unidades"
                precio_num = record.oferta_id.precio_metro * record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
                precio_num = round(precio_num, 4)
                precio = str(precio_num) + " €/unidad"
                if record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro > 0:
                    eton = record.oferta_id.precio_metro * 1000 / record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro
                
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
                cantidad_num_1 = und_pallet / 1000
                cantidad_num = record.num_pallets * und_pallet / 1000
                cantidad_num = round(cantidad_num, 4)
                cantidad = str(cantidad_num) + " millares"
                precio_num = record.oferta_id.precio_metro * record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad * 1000
                precio_num = round(precio_num, 4)
                precio = str(precio_num) + " €/millar"
                if record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro > 0:
                    eton = record.oferta_id.precio_metro * 1000 / record.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro
                
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
                peso_neto = record.oferta_id.kilos
                peso_bruto = peso_neto + 10
                cantidad_num_1 = peso_neto
                cantidad_num = record.num_pallets * peso_neto
                cantidad_num = round(cantidad_num, 4)
                cantidad = str(cantidad_num) + " kilos"
                precio_num = record.oferta_id.precio_kilo
                precio_num = round(precio_num, 4)
                precio = str(precio_num) + " €/kilo"
                eton = record.oferta_id.precio_kilo * 1000
            #Varios
            elif facturar == '5':
                cantidad_num_1 = und_pallet
                cantidad_num = record.num_pallets * und_pallet
                cantidad_num = round(cantidad_num, 4)
                cantidad = str(cantidad_num) + " unidades"
                precio_num = record.oferta_id.precio_varios
                precio_num = round(precio_num, 4)
                precio = str(precio_num) + " €/unidad"
                peso_neto = 0
                peso_bruto = 0
            
            importe = precio_num * cantidad_num
            
            """
            price_unit = 0
            if record.num_pallets > 0:
                price_unit = importe / record.num_pallets
            record.price_unit = price_unit
            record.product_uom_qty = record.num_pallets
            """
            
            record.codigo_cliente = codigo_cliente
            record.descripcion = descripcion
            record.und_pallet = und_pallet
            record.cantidad = cantidad
            record.precio = precio
            record.importe = importe
            record.peso_neto = peso_neto
            record.peso_bruto = peso_bruto
            record.eton = eton
            record.facturar = facturar
            record.precio_num = precio_num
            record.cantidad_num_1 = cantidad_num_1
            
            
    
    @api.depends('attribute_ids',)
    def _get_lots_sale(self):
        self.oferta_ids = self.env['stock.production.lot'].search([('sale_order_line_id.order_id', '=', lista_ids)])
    
    
    
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    #direccion_entrega_id = fields.Many2one('res.partner', string="Dirección Entrega 2")
    
    pedido_cliente = fields.Char('Número Pedido Cliente')
    fecha_entrega = fields.Date('Fecha Entrega Bemeco')
    fecha_cliente = fields.Date('Fecha del Pedido Cliente')
    fecha_entrega_cliente = fields.Date('Fecha Entrega del Pedido Cliente')
    provincia_id = fields.Many2one('res.country.state', string="Provincia")
    
    lot_ids = fields.Many2many('stock.production.lot', compute="_get_lots_sale", string="Lotes")

    num_pallets = fields.Integer('Pallets Pedido', compute="_get_num_pallets")
    peso_neto = fields.Integer('Peso Neto', compute="_get_num_pallets")
    peso_bruto = fields.Integer('Peso Bruto', compute="_get_num_pallets")
    peso_neto_mojado = fields.Integer('Peso Neto Mojado', compute="_get_num_pallets")
    peso_bruto_mojado = fields.Integer('Peso Bruto Mojado', compute="_get_num_pallets")
    eton = fields.Float('Eton', digits=(8, 1), compute="_get_num_pallets")
    importe_sin_descuento = fields.Float('Importe Sin Descuento', digits = (10, 2), compute="_get_num_pallets")
    importe_con_descuento = fields.Float('Importe Total', digits = (10, 2), compute="_get_num_pallets")
    haycodigo = fields.Boolean('Hay Código', compute = "_get_num_pallets")
    
    descuento_euros = fields.Float('Descuento Euros', digits = (10, 2), readonly = True, compute="_get_descuento")
    descuento_porcentaje = fields.Float('Descuento', digits = (10, 2), readonly = True, compute="_get_descuento")
    comercial_bueno_id = fields.Many2one('res.users', string='Comercial Bueno', compute="_get_descuento")
    no_editar = fields.Boolean('No Editar')
    actualizar = fields.Boolean('Actualizar')
    
    ESTADOS_SEL = [('0', 'NO CONFIRMADO'),     
                  ('1', 'CONFIRMADO'),
                  ('2', 'FABRICADO'),
                  ('3', 'ENTREGA PARCIAL'),
                  ('4', 'ENTREGA TOTAL'),
                  ]
    estado = fields.Selection(selection = ESTADOS_SEL, string = 'Estado pedido', store=True, compute="_get_estado_pedido")
    
    pendiente_facturar = fields.Float('Pendiente facturar', digits = (10, 2), readonly = True, compute="_get_pendiente_facturar")
    pendiente_cobrar = fields.Float('Pendiente cobrar', digits = (10, 2), readonly = True, compute="_get_pendiente_facturar")
    
    importe_riesgo = fields.Float('RIESGO PERMITIDO', digits = (12, 2), readonly = True, compute="_get_riesgo")
    
    
    
    @api.depends('partner_id')
    def _get_riesgo(self): 
        for record in self: 
            importe_riesgo = 0
            if record.partner_id:
                importe_riesgo = record.partner_id.importe_riesgo
            record.importe_riesgo = importe_riesgo
    
    
    @api.depends('invoice_ids', )
    def _get_pendiente_facturar(self):
        for record in self:
            pendiente_facturar = 0.0
            pendiente_cobrar = 0.0
            
            for invoice in record.invoice_ids:
                pendiente_cobrar = pendiente_cobrar + invoice.residual
                pendiente_facturar = pendiente_facturar + invoice.amount_untaxed
                
            pendiente_facturar = record.amount_untaxed - pendiente_facturar
            if pendiente_facturar < 0.0:
                pendiente_facturar = 0.0
                
            record.pendiente_facturar = pendiente_facturar
            record.pendiente_cobrar = pendiente_cobrar
    
    
    
    @api.onchange('actualizar', 'lot_ids', 'order_line')
    def _onchange_actualizar(self):
        for linea in self.order_line:
            linea.product_uom_qty = linea.num_pallets
            if linea.num_pallets > 0:
                linea.price_unit = linea.importe / linea.num_pallets
    
    
    
    @api.onchange('partner_shipping_id')
    def _onchange_provincia(self):
        if self.partner_id:
            self.provincia_id = self.partner_shipping_id.state_id

            
    
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
        if not self.fecha_entrega or self.fecha_entrega == None:
            raise exceptions.ValidationError('Error: es necesario introducir una fecha de entrega') 
        res = super(SaleOrder, self).action_confirm()
        for so in self:
            so.no_editar = True
            for line in so.order_line:
                line.no_editar = True
                if line.attribute_id:
                    line.attribute_id.no_editar = True
                if line.oferta_id:
                    line.oferta_id.no_editar = True
                if line.num_pallets > 0:
                    line.price_unit = line.importe / line.num_pallets
        return res
        
        

    #@api.depends('importe_con_descuento', 'importe_sin_descuento', 'partner_id.sale_discount')
    def _get_descuento(self):
        for record in self:
            porcentaje = record.partner_id.sale_discount
            euros = record.importe_sin_descuento - record.importe_con_descuento
            record.descuento_procentaje = porcentaje
            record.descuento_euros = euros
            record.comercial_bueno_id = record.partner_id.user_id.id
            
    
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
            
            """
            divisor = 150000
            peso_neto_mojado = (1 + (peso_neto / divisor)) * peso_neto
            peso_neto_mojado = int(peso_neto_mojado / 5) * 5
            peso_bruto_mojado = (1 + (peso_bruto / divisor)) * peso_bruto
            peso_bruto_mojado = int(peso_bruto_mojado / 5) * 5
            
            if peso_bruto < 24000:
                while peso_bruto_mojado > 24000:
                    divisor = divisor + 10000
                    peso_neto_mojado = (1 + (peso_neto / divisor)) * peso_neto
                    peso_neto_mojado = int(peso_neto_mojado / 5) * 5
                    peso_bruto_mojado = (1 + (peso_bruto / divisor)) * peso_bruto
                    peso_bruto_mojado = int(peso_bruto_mojado / 5) * 5
                    
                if peso_neto_mojado < peso_neto:
                    peso_neto_mojado = peso_neto
                if peso_bruto_mojado < peso_bruto:
                    peso_bruto_mojado = peso_bruto 
            else:
                peso_neto_mojado = peso_neto
                peso_bruto_mojado = peso_bruto
            """
            peso_neto_mojado = int(peso_neto * 1.05 / 10) * 10
            peso_bruto_mojado = int(peso_bruto * 1.05 / 10) * 10
            
            if peso_neto > 0:
                eton = eton / peso_neto
            record.num_pallets = num_pallets
            record.peso_neto = peso_neto
            record.peso_bruto = peso_bruto
            record.peso_neto_mojado = peso_neto_mojado
            record.peso_bruto_mojado = peso_bruto_mojado
            record.importe_sin_descuento = importe_sin_descuento
            record.importe_con_descuento = importe_con_descuento
            record.haycodigo = haycodigo
            record.eton = eton


    
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
                            estado = '2'
                            """
                            fabricado = True
                            for lot in record.lot_ids:
                                if lot.fabricado == False:
                                    fabricado = False
                                    break
                            if fabricado == True:
                            """
                                
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
                    if quantity2 >= 0:
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
