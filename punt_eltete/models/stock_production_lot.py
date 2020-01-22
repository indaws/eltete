
from odoo import fields, models, api



class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    
    sale_order_line_id = fields.Many2one('sale.order.line', string = "Línea de pedido")
    
    """
    SOBREESCRITOS BAJO
    """
    pallet_especial_id = fields.Many2one('product.caracteristica.pallet.especial', string = "Pallet especial")
    paletizado = fields.Integer('Paletizado')
    ancho_pallet = fields.Integer('Ancho Pallet')
    unidades = fields.Integer('Unidades')
    und_paquete = fields.Integer('Und Paquete')
    
    """
    PARA ELIMINAR
    """
    paquetes_fila = fields.Integer('Paquetes Fila')
    alto_fila = fields.Integer('Alto Fila')
    fila_max = fields.Integer('Fila Max')
    fila_buena = fields.Integer('Fila Buena')
    fabricado = fields.Boolean('Fabricado')
    sale_order_id = fields.Many2one('sale.order', string='Pedido', store=True, related='sale_order_line_id.order_id', readonly=True)
    attribute_id = fields.Many2one('sale.product.attribute', string = "Atributo")
    
    
    
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
    
    """
    #ref = fields.Char('Referencia Interna')
    #name = fields.Char('Lote/Nº Serie')
    referencia_id = fields.Many2one('product.referencia', string="Referencia", readonly=True, compute="_get_valores")
    oferta_id = fields.Many2one('sale.offer.oferta', string="Oferta")
    
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

    peso_neto = fields.Float('Peso Neto', digits=(10, 2), compute = "_get_valores")

   
    
    

    
    
    #CANTONERA
    cantonera_color = fields.Char('Cantonera Color', compute = "_get_valores")
    cantonera_forma_id = fields.Many2one('product.caracteristica.cantonera.forma', string="Forma", compute = "_get_valores")
    cantonera_especial_id = fields.Many2one('product.caracteristica.cantonera.especial', string="Especial", compute = "_get_valores")
    cantonera_impresion_id = fields.Many2one('product.caracteristica.cantonera.impresion', string="Impresión", compute = "_get_valores")
    cantonera_cliche_id = fields.Many2one('product.caracteristica.cliche', string="Cliché", compute = "_get_valores")
    fsc_id = fields.Many2one('product.caracteristica.fsc', string = "FSC", compute = "_get_valores")
    reciclable_id = fields.Many2one('product.caracteristica.reciclable', string = "Reciclable", compute = "_get_valores")
    paletizado = fields.Integer('Paletizado', compute="_get_valores")
    
    user_antonera_color_id = fields.Many2one('product.caracteristica.cantonera.color', string="Cambiar Cantonera Color")
    user_cantonera_forma_id = fields.Many2one('product.caracteristica.cantonera.forma', string="Cambiar Forma")
    user_cantonera_especial_id = fields.Many2one('product.caracteristica.cantonera.especial', string="Cambiar Especial")
    user_cantonera_impresion_id = fields.Many2one('product.caracteristica.cantonera.impresion', string="Cambiar Impresión")
    user_cantonera_cliche_id = fields.Many2one('product.caracteristica.cliche', string="Cambiar Cliché")
    user_fsc_id = fields.Many2one('product.caracteristica.fsc', string = "Cambiar FSC")
    user_reciclable_id = fields.Many2one('product.caracteristica.reciclable', string = "Cambiar Reciclable")
    PALETIZADO_SEL = [('1', 'Compacto (Normal)'),                 
                      ('2', 'Columnas'),
                      ]
    user_paletizado = fields.Selection(selection = PALETIZADO_SEL, string = 'Paletizado', default = '1')
    
    
    #PERFILU
    perfilu_color_id = fields.Many2one('product.caracteristica.perfilu.color', string="Perfil U Color", compute = "_get_valores")
    
    user_perfilu_color_id = fields.Many2one('product.caracteristica.perfilu.color', string="Cambiar Perfil U Color")
    
    #CANTONERA Y PERFILU
    inglete_id = fields.Many2one('product.caracteristica.inglete', string = "Tipo Inglete", compute = "_get_valores")
    inglete_num = fields.Integer('Numero de Ingletes', compute = "_get_valores")
    inglete_texto = fields.Char('Inglete Descripcion', compute = "_get_valores")
    
    user_inglete_id = fields.Many2one('product.caracteristica.inglete', string = "Cambiar Tipo Inglete")
    user_inglete_num = fields.Integer('Cambiar Numero de Ingletes')
    user_inglete_texto = fields.Char('Cambiar Inglete Descripcion')
    
    
    #SOLID BOARD
    plancha_color_id = fields.Many2one('product.caracteristica.planchacolor', string = "Plancha Color", compute = "_get_valores")
    
    user_plancha_color_id = fields.Many2one('product.caracteristica.planchacolor', string = "Cambiar Plancha Color")
    
    
    #FORMATO Y BOBINA
    papel_calidad_id = fields.Many2one('product.caracteristica.papelcalidad', string = "Papel Calidad", compute = "_get_valores")
    
    user_papel_calidad_id = fields.Many2one('product.caracteristica.papelcalidad', string = "Cambiar Papel Calidad")
    
    
    #SLIPSHEET, SOLIDBOARD Y FORMATO
    troquelado_id = fields.Many2one('product.caracteristica.troquelado', string = "Troquelado", compute = "_get_valores")
    
    user_troquelado_id = fields.Many2one('product.caracteristica.troquelado', string = "Cambiar Troquelado")
    
    
    #PARA TODOS
    pallet_especial_id = fields.Many2one('product.caracteristica.pallet.especial', string = "Pallet especial", compute="_get_valores")
    ancho_pallet = fields.Integer('Ancho Pallet', compute="_get_valores")
    und_paquete = fields.Integer('Und paquete', compute="_get_valores")
    unidades = fields.Integer('Unidades', compute="_get_valores")
    
    user_pallet_especial_id = fields.Many2one('product.caracteristica.pallet.especial', string = "Pallet especial")
    ANCHO_PALLET_SEL = [('1200', '1200'),     
                        ('1150', '1150'),
                        ('1000', '1000'),
                        ('800', '800'), 
                        ]
    user_ancho_pallet = fields.Selection(selection = ANCHO_PALLET_SEL, string = 'Ancho Pallet')
    user_und_paquete = fields.Integer('Und paquete')
    user_unidades = fields.Integer('Unidades')

    
    
    @api.multi
    def _get_peso(self):
        for record in self:
            peso_und = record.referencia_id.peso_metro * record.referencia_id.metros_unidad
            peso = peso_und * record.und_pallet
            record.peso_neto = peso
    
    
    
    @api.multi
    def _get_valores(self):
        for record in self:
            if record.user_cantonera_color_id:
                record.cantonera_color_id = record.user_cantonera_color_id
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.cantonera_color_id:
                    record.cantonera_color_id = record.sale_order_line_id.oferta_id.attribute_id.cantonera_color_id
            
            if record.user_cantonera_forma_id:
                record.cantonera_forma_id = record.user_cantonera_forma_id
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.cantonera_forma_id:
                    record.cantonera_color_id = record.sale_order_line_id.oferta_id.attribute_id.cantonera_forma_id
            
            if record.user_cantonera_especial_id:
                record.cantonera_especial_id = record.user_cantonera_especial_id
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.cantonera_especial_id:
                    record.cantonera_especial_id = record.sale_order_line_id.oferta_id.attribute_id.cantonera_especial_id
            
            if record.user_cantonera_impresion_id:
                record.cantonera_impresion_id = record.user_cantonera_impresion_id
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.cantonera_impresion_id:
                    record.cantonera_impresion_id = record.sale_order_line_id.oferta_id.attribute_id.cantonera_impresion_id
            
            if record.user_cantonera_cliche_id:
                record.cantonera_cliche_id = record.user_cantonera_cliche_id
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.cantonera_cliche_id:
                    record.cantonera_cliche_id = record.sale_order_line_id.oferta_id.attribute_id.cantonera_cliche_id
            
            if record.user_fsc_id:
                record.fsc_id = record.user_fsc_id
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.fsc_id:
                    record.fsc_id = record.sale_order_line_id.oferta_id.attribute_id.fsc_id
            
            if record.user_reciclable_id:
                record.reciclable_id = record.user_reciclable_id
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.reciclable_id:
                    record.reciclable_id = record.sale_order_line_id.oferta_id.attribute_id.reciclable_id
            
            if record.user_perfilu_color_id:
                record.perfilu_color_id = record.user_perfilu_color_id
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.perfilu_color_id:
                    record.perfilu_color_id = record.sale_order_line_id.oferta_id.attribute_id.perfilu_color_id
            
            if record.user_inglete_id:
                record.inglete_id = record.user_inglete_id
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.inglete_id:
                    record.inglete_id = record.sale_order_line_id.oferta_id.attribute_id.inglete_id
            
            if record.user_inglete_num:
                record.inglete_num = record.user_inglete_num
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.inglete_num:
                    record.inglete_num = record.sale_order_line_id.oferta_id.attribute_id.inglete_num
            
            if record.user_inglete_texto:
                record.inglete_texto = record.user_inglete_texto
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.inglete_texto:
                    record.inglete_texto = record.sale_order_line_id.oferta_id.attribute_id.inglete_texto
                    
            if record.user_plancha_color_id:
                record.plancha_color_id = record.user_plancha_color_id
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.plancha_color_id:
                    record.plancha_color_id = record.sale_order_line_id.oferta_id.attribute_id.plancha_color_id  
            
            if record.user_papel_calidad_id:
                record.papel_calidad_id = record.user_papel_calidad_id
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.papel_calidad_id:
                    record.papel_calidad_id = record.sale_order_line_id.oferta_id.attribute_id.papel_calidad_id
            
            if record.user_troquelado_id:
                record.troquelado_id = record.user_troquelado_id
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.troquelado_id:
                    record.troquelado_id = record.sale_order_line_id.oferta_id.attribute_id.troquelado_id
                    
            if record.user_paletizado:
                if record.user_paletizado == '1':
                    record.paletizado = 1
                elif record.user_paletizado == '2':
                    record.paletizado = 2
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.paletizado > 0:
                    record.paletizado = record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.paletizado
                    
            if record.user_pallet_especial_id:
                record.pallet_especial_id = record.user_pallet_especial_id
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.pallet_especial_id:
                    record.pallet_especial_id = record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.pallet_especial_id

            if record.user_ancho_pallet:
                if record.user_ancho_pallet == '1200':
                    record.ancho_pallet = 1200
                elif record.user_ancho_pallet == '1150':
                    record.ancho_pallet = 1150
                elif record.user_ancho_pallet == '1000':
                    record.ancho_pallet = 1000
                elif record.user_ancho_pallet == '800':
                    record.ancho_pallet = 800
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.ancho_pallet > 0:
                    record.ancho_pallet = record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.ancho_pallet
                    
            if record.user_und_paquete:
                record.und_paquete = record.user_und_paquete
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.und_paquete > 0:
                    record.und_paquete = record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.und_paquete
                    
            if record.user_unidades > 0
                record.unidadesrd.user_und_paquete
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.und_paquete > 0:
                    record.und_paquete = record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.und_paquete


    @api.multi
    def _crear_sin_pedido(self):
        self._crear_referencia()
        self._crear_producto()

    
    
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
                raise ValidationError("Error: Hay que indicar un valor en ancho")
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
                raise ValidationError("Error: Hay que indicar un valor en ancho")
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
                raise ValidationError("Error: Hay que indicar un valor en ancho")
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
                raise ValidationError("Error: Hay que indicar un valor en ancho")
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
                raise ValidationError("Error: Hay que indicar un valor en ancho")
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
                raise ValidationError("Error: Hay que indicar un valor en ancho")
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
            for prod in self.env['product.template'].search([('referencia_id', '=', self.referencia_id),
                                                             ]):
                product_id = prod
                
            if product_id == None:
                product_id = self.env['product.template'].create({'name': self.referencia_id.name, 
                                                                  'type': 'product',
                                                                  'purchase_ok': False,
                                                                  'sale_ok': True,
                                                                  'tracking': 'serial',
                                                                  'categ_id': self.referencia_id.type_id.id,
                                                                  'referencia_id':self.referencia_id.id, 
                                                                 })       
            
            
    """        
