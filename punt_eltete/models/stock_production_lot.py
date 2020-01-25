﻿
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    
    sale_order_line_id = fields.Many2one('sale.order.line', string = "Línea de pedido")
    referencia_id = fields.Many2one('product.referencia', string="Referencia")
    cliente_id = fields.Many2one('res.partner', string="Cliente")
    
    fabricado = fields.Boolean('Fabricado')
    
    """
    SOBREESCRITOS BAJO
    """
    #pallet_especial_id = fields.Many2one('product.caracteristica.pallet.especial', string = "Pallet especial")
    #paletizado = fields.Integer('Paletizado')
    #ancho_pallet = fields.Integer('Ancho Pallet')
    #unidades = fields.Integer('Unidades')
    #und_paquete = fields.Integer('Und Paquete')
    
    """
    PARA ELIMINAR
    """
    #paquetes_fila = fields.Integer('Paquetes Fila')
    #alto_fila = fields.Integer('Alto Fila')
    #fila_max = fields.Integer('Fila Max')
    #fila_buena = fields.Integer('Fila Buena')
    #attribute_id = fields.Many2one('sale.product.attribute', string = "Atributo")
    
    sale_order_id = fields.Many2one('sale.order', string='Pedido', store=True, related='sale_order_line_id.order_id', readonly=True)
    
    
    
    @api.multi
    def name_get(self):
        res = super(StockProductionLot, self).name_get()
        data = []
        for lot in self:
            display_value = lot.name
            if lot.unidades > 0:
                display_value = display_value + ' (' + str(lot.unidades) + ')'
            data.append((lot.id, display_value))
        return data
    
    
    """
    NUEVA VERSIÓN
    """
    
    
    #YA EXISTEN     ref = fields.Char('Referencia Interna')
    #YA EXISTEN     name = fields.Char('Lote/Nº Serie')
    
    
    #PARA CREAR EL LOTE SIN ORDEN DE PRODUCCIÓN
    type_id = fields.Many2one('product.category', string="Tipo de producto", required=True)
    is_cantonera = fields.Boolean('¿Es Cantonera?', related='type_id.is_cantonera')
    is_perfilu = fields.Boolean('¿Es Perfil U?', related='type_id.is_perfilu')
    is_slipsheet = fields.Boolean('¿Es Slip Sheet?', related='type_id.is_slipsheet')
    is_solidboard = fields.Boolean('¿Es Solid Board?', related='type_id.is_solidboard')
    is_formato = fields.Boolean('¿Es Formato?', related='type_id.is_formato')
    is_bobina = fields.Boolean('¿Es Bobina?', related='type_id.is_bobina')
    is_pieballet = fields.Boolean('¿Es Pie de Ballet?', related='type_id.is_pieballet')
    is_varios = fields.Boolean('¿Es Varios?', related='type_id.is_varios')
    is_flatboard = fields.Boolean('¿Es Flat Board?', related='type_id.is_flatboard')
    is_mprima_papel = fields.Boolean('¿Es mPrima Papel?', related='type_id.is_mprima_papel')
    
    TIPO_PIE = [('1', 'Alto 100 con Adhesivo'), 
               ('2', 'Alto 100 sin Adhesivo'),
               ('3', 'Alto 60 con Adhesivo'),                 
               ('4', 'Alto 60 sin Adhesivo'),        
               ]
    pie = fields.Selection(selection = TIPO_PIE, string = 'Tipo Pie', default = '1')
    ala_1 = fields.Integer('Ala 1 / Solapa')
    ancho = fields.Integer('Ancho')
    ala_2 = fields.Integer('Ala 2')
    grosor_2 = fields.Float('Grosor 2', digits=(8,2))
    ala_3 = fields.Integer('Solapa 3')
    longitud = fields.Integer('Longitud')
    ala_4 = fields.Integer('Solapa 4')
    grosor_1 = fields.Float('Grosor 1', digits=(8,1))    
    diametro = fields.Integer('Diámetro')
    gramaje = fields.Integer('Gramaje')
    tipo_varios_id = fields.Many2one('product.caracteristica.varios', string="Tipo varios")


    #OCULTOS
    cambios_fabricacion = fields.Boolean('Cambios Fabricación', readonly = True, compute = "_get_valores")
    cambios_cliente = fields.Boolean('Cambios Cliente', readonly = True, compute = "_get_cliente")


    #PARA TODOS
    hora_inicio = fields.Datetime('Hora Inicio Fabricación')
    hora_fin = fields.Datetime('Hora Fin Fabricación')
    pallet_sage = fields.Char('Pallet Sage')
    maquina = fields.Integer('Máquina')
    cambiar_etiqueta = fields.Boolean('Cambiar Etiqueta', readonly = True, compute = "_get_etiqueta")
    peso_neto = fields.Float('Peso Neto', digits=(10, 2), readonly = True, compute = "_get_peso")
    fecha_entrada = fields.Date('Fecha Entrada')
    fecha_salida = fields.Date('Fecha Salida')
    disponible = fields.Boolean('Disponible', readonly = True, compute = "_get_disponible")

    
    #CANTONERA
    cantonera_color_id = fields.Char('Cantonera Color', readonly = True, compute = "_get_valores")
    cantonera_forma_id = fields.Many2one('product.caracteristica.cantonera.forma', string="Forma", readonly = True, compute = "_get_valores")
    cantonera_especial_id = fields.Many2one('product.caracteristica.cantonera.especial', string="Especial", readonly = True, compute = "_get_valores")
    cantonera_impresion_id = fields.Many2one('product.caracteristica.cantonera.impresion', string="Impresión", readonly = True, compute = "_get_valores")
    cantonera_cliche_id = fields.Many2one('product.caracteristica.cliche', string="Cliché", readonly = True, compute = "_get_valores")
    fsc_id = fields.Many2one('product.caracteristica.fsc', string = "FSC", readonly = True, compute = "_get_valores")
    reciclable_id = fields.Many2one('product.caracteristica.reciclable', string = "Reciclable", readonly = True, compute = "_get_valores")
    paletizado = fields.Integer('Paletizado', compute="_get_valores")
    
    user_cantonera_color_id = fields.Many2one('product.caracteristica.cantonera.color', string="Cambiar Cantonera Color")
    user_cantonera_forma_id = fields.Many2one('product.caracteristica.cantonera.forma', string="Cambiar Forma")
    user_cantonera_especial_id = fields.Many2one('product.caracteristica.cantonera.especial', string="Cambiar Especial")
    user_cantonera_impresion_id = fields.Many2one('product.caracteristica.cantonera.impresion', string="Cambiar Impresión")
    user_cantonera_cliche_id = fields.Many2one('product.caracteristica.cliche', string="Cambiar Cliché")
    user_fsc_id = fields.Many2one('product.caracteristica.fsc', string = "Cambiar FSC")
    user_reciclable_id = fields.Many2one('product.caracteristica.reciclable', string = "Cambiar Reciclable")
    PALETIZADO_SEL = [('1', 'Compacto (Normal)'),                 
                      ('2', 'Columnas'),
                      ]
    user_paletizado = fields.Selection(selection = PALETIZADO_SEL, string = 'Paletizado')
    
    
    #PERFILU
    perfilu_color_id = fields.Many2one('product.caracteristica.perfilu.color', string="Perfil U Color", readonly = True, compute = "_get_valores")
    
    user_perfilu_color_id = fields.Many2one('product.caracteristica.perfilu.color', string="Cambiar Perfil U Color")
    
    #CANTONERA Y PERFILU
    inglete_id = fields.Many2one('product.caracteristica.inglete', string = "Tipo Inglete", readonly = True, compute = "_get_valores")
    inglete_num = fields.Integer('Numero de Ingletes', readonly = True, compute = "_get_valores")
    inglete_texto = fields.Char('Inglete Descripcion', readonly = True, compute = "_get_valores")
    
    user_inglete_id = fields.Many2one('product.caracteristica.inglete', string = "Cambiar Tipo Inglete")
    user_inglete_num = fields.Integer('Cambiar Numero de Ingletes')
    user_inglete_texto = fields.Char('Cambiar Inglete Descripcion')
    
    
    #SOLID BOARD
    plancha_color_id = fields.Many2one('product.caracteristica.planchacolor', string = "Plancha Color", readonly = True, compute = "_get_valores")
    
    user_plancha_color_id = fields.Many2one('product.caracteristica.planchacolor', string = "Cambiar Plancha Color")
    
    
    #FORMATO Y BOBINA
    papel_calidad_id = fields.Many2one('product.caracteristica.papelcalidad', string = "Papel Calidad", readonly = True, compute = "_get_valores")
    
    user_papel_calidad_id = fields.Many2one('product.caracteristica.papelcalidad', string = "Cambiar Papel Calidad")
    
    
    #SLIPSHEET, SOLIDBOARD Y FORMATO
    troquelado_id = fields.Many2one('product.caracteristica.troquelado', string = "Troquelado", readonly = True, compute = "_get_valores")
    
    user_troquelado_id = fields.Many2one('product.caracteristica.troquelado', string = "Cambiar Troquelado")
    
    
    #PARA TODOS
    pallet_especial_id = fields.Many2one('product.caracteristica.pallet.especial', string = "Pallet especial", readonly = True, compute="_get_valores")
    ancho_pallet = fields.Integer('Ancho Pallet', readonly = True, compute="_get_valores")
    und_paquete = fields.Integer('Und paquete', readonly = True, compute="_get_valores")
    unidades = fields.Integer('Unidades', readonly = True, compute="_get_valores")
    
    user_pallet_especial_id = fields.Many2one('product.caracteristica.pallet.especial', string = "Pallet especial")
    ANCHO_PALLET_SEL = [('1200', '1200'),     
                        ('1150', '1150'),
                        ('1000', '1000'),
                        ('800', '800'), 
                        ]
    user_ancho_pallet = fields.Selection(selection = ANCHO_PALLET_SEL, string = 'Ancho Pallet')
    user_und_paquete = fields.Integer('Und paquete')
    user_unidades = fields.Integer('User Unidades')

    
    
    @api.depends('cliente_id', 'fecha_entrada', 'fecha_salida')
    def _get_disponible(self):
        for record in self:
            disponible = False
            if record.fecha_entrada:
                if record.fecha_salida:
                    x = 0
                elif record.cliente_id:
                    x = 0
                else:
                    disponible = True
                
            record.disponible = disponible
    
    
    
    @api.depends('cambios_fabricacion', 'cambios_cliente')
    def _get_etiqueta(self):
        for record in self:
            cambiar_etiqueta = False
            if record.cambios_fabricacion == True or record.cambios_cliente == True:
                cambiar_etiqueta = True
                
            record.cambiar_etiqueta = True



    @api.onchange('cliente_id')
    def _onchange_cliente(self):
        self.cambios_cliente = True
    
    
    
    @api.depends('referencia_id', 'unidades')
    def _get_peso(self):
        for record in self:
            peso_neto = 0
            if record.referencia_id and record.unidades > 0:
                peso_und = record.referencia_id.peso_metro * record.referencia_id.metros_unidad
                peso_neto = peso_und * record.unidades
            record.peso_neto = peso_neto
    
    
    
    @api.multi
    def _get_valores(self):
        for record in self:
            cambios_fabricacion = False
        
            if record.user_cantonera_color_id:
                record.cantonera_color_id = record.user_cantonera_color_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            if record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.cantonera_color_id:
                    record.cantonera_color_id = record.sale_order_line_id.oferta_id.attribute_id.cantonera_color_id.id
            
            if record.user_cantonera_forma_id:
                record.cantonera_forma_id = record.user_cantonera_forma_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.cantonera_forma_id:
                    record.cantonera_color_id = record.sale_order_line_id.oferta_id.attribute_id.cantonera_forma_id.id
            
            if record.user_cantonera_especial_id:
                record.cantonera_especial_id = record.user_cantonera_especial_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.cantonera_especial_id:
                    record.cantonera_especial_id = record.sale_order_line_id.oferta_id.attribute_id.cantonera_especial_id.id
            
            if record.user_cantonera_impresion_id:
                record.cantonera_impresion_id = record.user_cantonera_impresion_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.cantonera_impresion_id:
                    record.cantonera_impresion_id = record.sale_order_line_id.oferta_id.attribute_id.cantonera_impresion_id.id
            
            if record.user_cantonera_cliche_id:
                record.cantonera_cliche_id = record.user_cantonera_cliche_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.cantonera_cliche_id:
                    record.cantonera_cliche_id = record.sale_order_line_id.oferta_id.attribute_id.cantonera_cliche_id.id
            
            if record.user_fsc_id:
                record.fsc_id = record.user_fsc_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.fsc_id:
                    record.fsc_id = record.sale_order_line_id.oferta_id.attribute_id.fsc_id.id
            
            if record.user_reciclable_id:
                record.reciclable_id = record.user_reciclable_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.reciclable_id:
                    record.reciclable_id = record.sale_order_line_id.oferta_id.attribute_id.reciclable_id.id
            
            if record.user_perfilu_color_id:
                record.perfilu_color_id = record.user_perfilu_color_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.perfilu_color_id:
                    record.perfilu_color_id = record.sale_order_line_id.oferta_id.attribute_id.perfilu_color_id.id
            
            if record.user_inglete_id:
                record.inglete_id = record.user_inglete_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.inglete_id:
                    record.inglete_id = record.sale_order_line_id.oferta_id.attribute_id.inglete_id.id
            
            if record.user_inglete_num > 0:
                record.inglete_num = record.user_inglete_num
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.inglete_num > 0:
                    record.inglete_num = record.sale_order_line_id.oferta_id.attribute_id.inglete_num
            
            if record.user_inglete_texto:
                record.inglete_texto = record.user_inglete_texto
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.inglete_texto:
                    record.inglete_texto = record.sale_order_line_id.oferta_id.attribute_id.inglete_texto
                    
            if record.user_plancha_color_id:
                record.plancha_color_id = record.user_plancha_color_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.plancha_color_id:
                    record.plancha_color_id = record.sale_order_line_id.oferta_id.attribute_id.plancha_color_id.id
            
            if record.user_papel_calidad_id:
                record.papel_calidad_id = record.user_papel_calidad_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.papel_calidad_id:
                    record.papel_calidad_id = record.sale_order_line_id.oferta_id.attribute_id.papel_calidad_id.id
            
            if record.user_troquelado_id:
                record.troquelado_id = record.user_troquelado_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.troquelado_id:
                    record.troquelado_id = record.sale_order_line_id.oferta_id.attribute_id.troquelado_id.id
                    
            if record.user_paletizado:
                if record.user_paletizado == '1':
                    record.paletizado = 1
                elif record.user_paletizado == '2':
                    record.paletizado = 2
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.paletizado > 0:
                    record.paletizado = record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.paletizado
                    
            if record.user_pallet_especial_id:
                record.pallet_especial_id = record.user_pallet_especial_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.pallet_especial_id:
                    record.pallet_especial_id = record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.pallet_especial_id.id

            if record.user_ancho_pallet:
                if record.user_ancho_pallet == '1200':
                    record.ancho_pallet = 1200
                elif record.user_ancho_pallet == '1150':
                    record.ancho_pallet = 1150
                elif record.user_ancho_pallet == '1000':
                    record.ancho_pallet = 1000
                elif record.user_ancho_pallet == '800':
                    record.ancho_pallet = 800
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.ancho_pallet > 0:
                    record.ancho_pallet = record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.ancho_pallet
                    
            if record.user_und_paquete > 0:
                record.und_paquete = record.user_und_paquete
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.und_paquete > 0:
                    record.und_paquete = record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.und_paquete
                    
            if record.user_unidades > 0:
                record.unidades = record.user_unidades
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.und_pallet > 0:
                    record.unidades = record.sale_order_line_id.und_pallet
            
            
            record.cambios_fabricacion = cambios_fabricacion



    @api.multi
    def crear_sin_pedido(self):
        for record in self:
            record._crear_referencia()
            record.product_id = record._crear_producto()

    
    
    @api.multi
    def _crear_referencia(self):
    
        if self.type_id.is_varios == True:
            
            if not self.tipo_varios_id:
                raise ValidationError("Error: Hay que indicar un valor de Varios")

            referencia_id, error = self.type_id.create_prod_varios(self.tipo_varios_id)

            if not referencia_id:
                raise ValidationError(error)

            self.referencia_id = referencia_id    
            
            
            
        if self.type_id.is_cantonera == True:

            if not self.ala_1 or self.ala_1 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ALA 1")
            if not self.ala_2 or self.ala_2 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ALA 2")
            if not self.grosor_2 or self.grosor_2 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en GROSOR")
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
                
            referencia_id, error = self.type_id.create_prod_cantonera(self.ala_1, self.ala_2, self.grosor_2, self.longitud)
            
            if not referencia_id:
                raise ValidationError(error)
 
            self.referencia_id = referencia_id    
            
            
            
        if self.type_id.is_perfilu == True:
        
            if not self.ala_1 or self.ala_1 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ALA 1")
            if not self.ancho or self.ancho <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ANCHO")
            if not self.ala_2 or self.ala_2 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ALA 2")
            if not self.grosor_2 or self.grosor_2 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en GROSOR")
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
                
            referencia_id, error = self.type_id.create_prod_perfilu(self.ala_1, self.ancho, self.ala_2, self.grosor_2, self.longitud)

            if not referencia_id:
                raise ValidationError(error)
                 
            self.referencia_id = referencia_id    
            
            
            
        if self.type_id.is_slipsheet == True:
            
            if not self.ancho or self.ancho <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ANCHO")
            if not self.grosor_1 or self.grosor_1 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en GROSOR")
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
                
            referencia_id, error = self.type_id.create_prod_slipsheet(self.ala_1, self.ancho, self.ala_2, self.grosor_1, self.longitud, self.ala_3, self.ala_4)

            if not referencia_id:
                raise ValidationError(error)
                
            self.referencia_id = referencia_id    
            
            
            
        if self.type_id.is_solidboard == True:
        
            if not self.ancho or self.ancho <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ANCHO")
            if not self.grosor_1 or self.grosor_1 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en GROSOR")
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
                
            referencia_id, error = self.type_id.create_prod_solidboard(self.ancho, self.grosor_1, self.longitud)

            if not referencia_id:
                raise ValidationError(error)
                
            self.referencia_id = referencia_id    

            
            
        if self.type_id.is_formato == True:
        
            if not self.ancho or self.ancho <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ANCHO")
            if not self.gramaje or self.gramaje <= 0:
                raise ValidationError("Error: Hay que indicar un valor en GRAMAJE")
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
                
            referencia_id, error = self.type_id.create_prod_formato(self.ancho, self.longitud, self.gramaje)

            if not referencia_id:
                raise ValidationError(error)
                
            self.referencia_id = referencia_id    
            
            
            
        if self.type_id.is_bobina == True:
        
            if not self.ancho or self.ancho <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ANCHO")
            if not self.gramaje or self.gramaje <= 0:
                raise ValidationError("Error: Hay que indicar un valor en GRAMAJE")
            if not self.diametro or self.diametro <= 0:
                raise ValidationError("Error: Hay que indicar un valor en DIÁMETRO")
                
            referencia_id, error = self.type_id.create_prod_bobina(self.ancho, self.diametro, self.gramaje)
            
            if not referencia_id:
                raise ValidationError(error)
                
            if self.check_duplicado_referencia(referencia_id):
                raise ValidationError("Error: Este cliente ya tiene esta referencia creada")
                
            self.referencia_id = referencia_id    
            
            
            
        if self.type_id.is_pieballet == True:
        
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
            if not self.pie:
                raise ValidationError("Error: Hay que indicar un valor en PIE")
                
            referencia_id, error = self.type_id.create_prod_pieballet(self.longitud, self.pie)

            if not referencia_id:
                raise ValidationError(error)
                
            self.referencia_id = referencia_id    
            
            
            
        if self.type_id.is_flatboard == True:
        
            if not self.ancho or self.ancho <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ANCHO")
            if not self.grosor_1 or self.grosor_1 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en GROSOR")
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
                
            referencia_id, error = self.type_id.create_prod_flatboard(self.ancho, self.grosor_1, self.longitud)

            if not referencia_id:
                raise ValidationError(error)
                
            self.referencia_id = referencia_id    

            
            
    @api.multi
    def _crear_producto(self):
        for record in self:
            product_id = None
            for prod in self.env['product.template'].search([('referencia_id', '=', self.referencia_id.id),
                                                             ]):
                product_id = prod
                
            if product_id == None:
                es_vendido = False
                es_comprado = False
                tipo_producto = ''
                cuenta_ingresos_code = -1
                cuenta_gastos_code = -1
                
                if record.is_cantonera == True:
                    es_vendido = True
                    es_comprado = False
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70100001
                    cuenta_gastos_code = -1
                if record.is_perfilu == True:
                    es_vendido = True
                    es_comprado = True
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000008
                    cuenta_gastos_code = 60000003
                if record.is_slipsheet == True:
                    es_vendido = True
                    es_comprado = False
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70100009
                    cuenta_gastos_code = -1
                if record.is_solidboard == True:
                    es_vendido = True
                    es_comprado = False
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000011
                    cuenta_gastos_code = -1
                if record.is_formato == True:
                    es_vendido = True
                    es_comprado = True
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000004
                    cuenta_gastos_code = 60000004
                if record.is_bobina == True:
                    es_vendido = True
                    es_comprado = True
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000004
                    cuenta_gastos_code = 60000004
                if record.is_pieballet == True:
                    es_vendido = True
                    es_comprado = True
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000002
                    cuenta_gastos_code = 60000005
                if record.is_flatboard == True:
                    es_vendido = True
                    es_comprado = True
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000005
                    cuenta_gastos_code = 60000007
                if record.is_varios == True:
                    es_vendido = True
                    es_comprado = True
                    tipo_producto = 'consu'
                    cuenta_gastos_code = -1
                    if record.tipo_varios_id:
                        cuenta_ingresos_code = record.tipo_varios_id.number
                if record.is_mprima_papel == True:
                    es_vendido = True
                    es_comprado = False
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000004
                    cuenta_gastos_code = 60100001
                
                product_id = self.env['product.template'].create({'name': record.referencia_id.name, 
                                                                  'type': tipo_producto,
                                                                  'purchase_ok': es_comprado,
                                                                  'sale_ok': es_vendido,
                                                                  'tracking': 'serial',
                                                                  'categ_id': record.type_id.id,
                                                                  'referencia_id':record.referencia_id.id, 
                                                                  #'property_account_income_id': 
                                                                  #'property_account_expense_id': 
                                                                 })
            return product_id.product_variant_id.id,
            
    
