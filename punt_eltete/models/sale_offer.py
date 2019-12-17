
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

    
class sale_referencia_cliente(models.Model):
    _name = 'sale.referencia.cliente'

    name = fields.Char(string='Ref cliente nombre', required=True, default=lambda self: "/")
    
    
    partner_id = fields.Many2one('res.partner', string="Cliente", required=True)
    user_id = fields.Many2one('res.users', string="Comercial", default=lambda self: self.env.user, required=True)
    date = fields.Date('Fecha', default=fields.Date.today(), required=True, copy=False)
    
    ETAPAS = [('BOR','BORRADOR'),   
              ('REF','REFERENCIA'),
              ('RCL','REF CLIENTE'),
              ('CAN','CANCELADA'),
             ]
    state = fields.Selection(selection=ETAPAS, string='Estado', default='BOR', track_visibility='onchange')
    
    
    
    
    #REFERENCIAS
    type_id = fields.Many2one('product.category', string="Tipo de producto", required=True)
    
    is_cantonera = fields.Boolean('¿Es Cantonera?', related='type_id.is_cantonera')
    is_perfilu = fields.Boolean('¿Es Perfil U?', related='type_id.is_perfilu')
    is_slipsheet = fields.Boolean('¿Es Slip Sheet?', related='type_id.is_slipsheet')
    is_solidboard = fields.Boolean('¿Es Solid Board?', related='type_id.is_solidboard')
    is_formato = fields.Boolean('¿Es Formato?', related='type_id.is_formato')
    is_bobina = fields.Boolean('¿Es Bobina?', related='type_id.is_bobina')
    is_pieballet = fields.Boolean('¿Es Pie de Ballet?', related='type_id.is_pieballet')
    is_varios = fields.Boolean('¿Es Varios?', related='type_id.is_varios')
    
    
    ala_1 = fields.Integer('Ala 1')
    base = fields.Integer('Base')
    ancho = fields.Integer('Ancho')
    ala_2 = fields.Integer('Ala 2')
    grosor = fields.Float('Grosor')
    longitud = fields.Integer('Longitud')
    alas = fields.Integer('Alas')
    ala_3 = fields.Integer('Solapa 3')
    ala_4 = fields.Integer('Solapa 4')
    
    diametro = fields.Integer('Diámetro')
    gramaje = fields.Integer('Gramaje')
    
    
    TIPO_PIE = [('1', 'Alto 100 con Adhesivo'), 
               ('2', 'Alto 100 sin Adhesivo'),
               ('3', 'Alto 60 con Adhesivo'),                 
               ('4', 'Alto 60 sin Adhesivo'),         #La coma final?
               ]
    pie = fields.Selection(selection = TIPO_PIE, string = 'Tipo Pie')
    
    ancho_interior = fields.Integer('Ancho Interior')
    ancho_superficie = fields.Integer('Ancho Superficie')
    
    #varios
    peso_metro_user = fields.Float('Peso Metro', digits = (10,4))
    metros_unidad_user = fields.Float('Metros Unidad', digits = (10,4))
    referencia_id = fields.Many2one('product.referencia', string="Referencia", readonly=True)
    
    
    #product_id = fields.Many2one('product.template', string="Producto", readonly=True)
    
    
    #REFERENCIA CLIENTE
    pallet_especial_id = fields.Many2one('product.caracteristica.pallet.especial', string = "Pallet especial")
    
    PALETIZADO_SEL = [('1', 'Compacto'),                 
                      ('2', 'Columnas'),
                      ]
    paletizado_cliente = fields.Selection(selection = PALETIZADO_SEL, string = 'Paletizado Cliente', default = '1')
    
    ANCHO_PALLET_SEL = [('1200', '1200'),     
                        ('1150', '1150'),
                        ('1000', '1000'),
                        ('800', '800'), 
                        ]
    ancho_pallet_cliente = fields.Selection(selection = ANCHO_PALLET_SEL, string = 'Ancho Pallet Cliente')
    contenedor = fields.Boolean('Contenedor', default = False)
    
    und_paquete_cliente = fields.Integer('Und pallet cliente')
    und_pallet_cliente = fields.Integer('Unidades Exactas')
    alto_max_cliente = fields.Integer('Alto máximo cliente')
    peso_max_cliente = fields.Integer('Peso máximo cliente')
    
    comentario_paletizado = fields.Text('Comentario Paletizado')
    PRECIO_SEL = [('1', 'metro / metro2'),     
                  ('2', 'unidad'),
                  ('3', 'millar'),
                  ('4', 'kilos'), 
                  ]
    precio_cliente = fields.Selection(selection = PRECIO_SEL, string = 'Facturar por:')


    
    #CALCULOS
    paletizado = fields.Integer('Paletizado', compute="_get_valores")
    ancho_pallet = fields.Integer('Ancho Pallet', compute="_get_valores")
    und_paquete = fields.Integer('Und Paquete', compute="_get_valores")
    paquetes_fila = fields.Integer('Paquetes Fila', compute="_get_valores")
    alto_fila = fields.Integer('Alto Fila', compute="_get_valores")
    
    
    attribute_ids = fields.One2many('sale.product.attribute', 'referencia_cliente_id', string="Atributos", copy=True)
    #oferta_ids = fields.Many2many('sale.offer.oferta', string="Ofertas de la referencia", compute="_get_ofertas", readonly=True)
    oferta_ids = fields.One2many('sale.offer.oferta', 'referencia_cliente_id', string="Ofertas")
    
    
    
    @api.depends('type_id',)
    def _get_valores(self):
        paletizado = 0
        ancho_pallet = 0
        und_paquete = 0
        paquetes = 0
        alto_fila = 0

        if self.referencia_id:
            #Varios
            if self.type_id.is_varios == True:
                if self.und_paquete_cliente > 0:
                    und_paquete = self.und_paquete_cliente
                paquetes = 1
                alto_fila = 10
            #Cantonera
            elif self.type_id.is_cantonera == True:
                paletizado = 1
                if self.paletizado_cliente == '2':
                    paletizado = 2
                    if self.und_paquete_cliente > 0:     
                        paletizado = 1
                    if self.und_pallet_cliente > 0:     
                        paletizado = 1
                alto_fila = (self.referencia_id.ala_1 + self.referencia_id.ala_2) * 0.7071
                        
                if paletizado == 2:
                    ancho_pallet = 1150
                if self.contenedor == True and self.referencia_id.longitud > 2300:
                    ancho_pallet = 1000
                if self.ancho_pallet_cliente:
                    if int(self.ancho_pallet_cliente) < ancho_pallet:
                        ancho_pallet = self.ancho_pallet_cliente
                        
                ##Unidades paquetes_fila
                if self.referencia_id.longitud < 250:
                    und_paquete = 4000
                        
                elif self.und_paquete_cliente > 0:
                    und_paquete = self.und_paquete_cliente
                #compacto    
                elif paletizado == 1:
                    und_paquete = 25
                    if self.referencia_id.grosor >= 5:
                        und_paquete = 10
                    elif self.referencia_id.grosor >= 4:
                        und_paquete = 20
                    pesoPaquete = und_paquete * self.referencia_id.peso_metro * self.referencia_id.metros_unidad
                    while pesoPaquete > 20:
                        und_paquete = und_paquete - 5
                        pesoPaquete = und_paquete * self.referencia_id.peso_metro * self.referencia_id.metros_unidad
                #Columnas
                elif paletizado == 2:
                    mediaAlas = (self.referencia_id.ala_1 + self.referencia_id.ala_2) / 2
                    undColumna = int(((ancho_pallet - 10) / 4 - 0.7071 * mediaAlas) / (self.referencia_id.grosor * 1.5))
                    paquetesColumna = 2
                    und_paquete = int(undColumna / paquetesColumna)
                    pesoPaquete = und_paquete * self.referencia_id.peso_metro * self.referencia_id.metros_unidad
                    while pesoPaquete > 20:
                        paquetesColumna = paquetesColumna + 1
                        und_paquete = int(undColumna / paquetesColumna)
                        pesoPaquete = und_paquete * self.referencia_id.peso_metro * self.referencia_id.metros_unidad
                ##Fin unidades paquete
                
                ##Paquetes filas
                mediaAlas = (self.referencia_id.ala_1 + self.referencia_id.ala_2) / 2
                if paletizado == 1:
                    if self.referencia_id.grosor != 0:
                        undFilaMax = int((ancho_pallet - 0.7071 * mediaAlas) / (self.referencia_id.grosor * 1.5))
                        paquetes = int(undFilaMax / und_paquete)
                elif paletizado == 2:
                    undColumna = int(((ancho_pallet - 10) / 4 - 0.7071 * mediaAlas) / (self.referencia_id.grosor * 1.5))
                    paquetes = undColumna / und_paquete
                    
                #Dobles, Triples
                repetido = 1
                if self.referencia_id.longitud == 250:
                    repetido = 4
                elif self.referencia_id.longitud > 250 and self.referencia_id.longitud <= 350:
                    repetido = 3
                elif self.referencia_id.longitud > 350 and self.referencia_id.longitud <= 650:
                    repetido = 2
                paquetes = paquetes * repetido
                ##Fin paquetes filas
                    
            #Perfil U
            elif self.type_id.is_perfilu == True:
                if self.ancho_pallet_cliente:
                    ancho_pallet = int(self.ancho_pallet_cliente)
                    paquetes = int(ancho_pallet / (self.referencia_id.ancho + self.referencia_id.grosor * 3))
                    if self.longitud <= 600:
                        paquetes = paquetes * 2
                
                und_paquete = 2
                alto_fila = self.referencia_id.ala_1 + self.referencia_id.grosor
                
            #Slip Sheets
            elif self.type_id.is_slipsheet == True:
                und_paquete = 50
                lado1 = 1
                lado2 = 1
                if self.referencia_id.ancho <= 650:
                    lado1 = int(1300 / self.referencia_id.ancho)
                if self.referencia_id.longitud <= 650:
                    lado2 = int(1300 / self.referencia_id.longitud)
                paquetes = lado1 * lado2
                
                alto_fila = self.referencia_id.grosor * 50
                
            #Solid Board
            elif self.type_id.is_solidboard == True:
                und_paquete = 50
                lado1 = 1
                lado2 = 1
                if self.referencia_id.ancho <= 650:
                    lado1 = int(1300 / self.referencia_id.ancho)
                if self.referencia_id.longitud <= 650:
                    lado2 = int(1300 / self.referencia_id.longitud)
                paquetes = lado1 * lado2
                alto_fila = self.referencia_id.grosor * 50
                
            #Formato
            elif self.type_id.is_formato == True:
                und_paquete = 50
                if self.und_paquete_cliente > 0:
                    und_paquete = self.und_paquete_cliente
                lado1 = 1
                lado2 = 1
                if self.referencia_id.ancho <= 650:
                    lado1 = int(1300 / self.referencia_id.ancho)
                if self.referencia_id.longitud <= 650:
                    lado2 = int(1300 / self.referencia_id.longitud)
                paquetes = lado1 * lado2
                if self.und_paquete_cliente > 0:
                    alto_fila = self.referencia_id.gramaje * 1.4 * self.und_paquete_cliente
                else:
                    alto_fila = self.referencia_id.grosor * 50
            #Bobina
            elif self.type_id.is_bobina == True:
                und_paquete = 1
                if self.referencia_id.diametro > 650:
                    paquetes = 1
                else:
                    lado1 = int(1300 / self.referencia_id.diametro)
                    lado2 = int(1100 / self.referencia_id.diametro)
                    paquetes = lado1 * lado2
                    
                alto_fila = self.referencia_id.ancho
                
            #Pie de Pallet
            elif self.type_id.is_pieballet == True:
                und_paquete = 1
                if self.longitud == 190:
                    paquetes = 65
                elif self.longitud >= 200 and self.longitud < 350:
                    paquetes = 52
                elif self.longitud >= 350 and self.longitud < 400:
                    paquetes = 39
                elif self.longitud >= 400 and self.longitud < 660:
                    paquetes = 26
                else:
                    paquetes = 13
                    
                if self.pie == "1" or self.pie == "2":
                    alto_fila = 100
                elif self.pie == "3" or self.pie == "4":
                    alto_fila = 60
    
    
        self.paletizado = paletizado
        self.ancho_pallet = ancho_pallet
        self.und_paquete = und_paquete
        self.paquetes_fila = paquetes
        self.alto_fila = alto_fila
    
    
    
    
    
    

    @api.depends('attribute_ids',)
    def _get_ofertas(self):
        lista_ids = []
        for att in self.attribute_ids:
            lista_ids.append(att.id)
        self.oferta_ids = self.env['sale.offer.oferta'].search([('attribuite_id', 'in', lista_ids)])

    
    
    @api.multi
    def bor_to_ref(self):
        if self.type_id.is_cantonera == True:
        
            if not self.ala_1 or self.ala_1 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ALA 1")
            if not self.ala_2 or self.ala_2 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ALA 2")
            if not self.grosor or self.grosor <= 0:
                raise ValidationError("Error: Hay que indicar un valor en GROSOR")
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
                
            referencia_id, error = self.type_id.create_prod_cantonera(self.ala_1, self.ala_2, self.grosor, self.longitud)
            
            if not referencia_id:
                raise ValidationError(error)
            self.referencia_id = referencia_id    
            self.state = 'REF'
            self.name = self.referencia_id.name
            
            
        if self.type_id.is_perfilu == True:
        
            if not self.ala_1 or self.ala_1 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ALA 1")
            if not self.ancho or self.ancho <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ancho")
            if not self.ala_2 or self.ala_2 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ALA 2")
            if not self.grosor or self.grosor <= 0:
                raise ValidationError("Error: Hay que indicar un valor en GROSOR")
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
                
            referencia_id, error = self.type_id.create_prod_perfilu(self.ala_1, self.ancho, self.ala_2, self.grosor, self.longitud)
            
            if not referencia_id:
                raise ValidationError(error)
            self.referencia_id = referencia_id    
            self.state = 'REF'
            self.name = self.referencia_id.name
            
            
        if self.type_id.is_slipsheet == True:
        
            
            if not self.ancho or self.ancho <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ancho")
            if not self.grosor or self.grosor <= 0:
                raise ValidationError("Error: Hay que indicar un valor en GROSOR")
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
                
            referencia_id, error = self.type_id.create_prod_slipsheet(self.ala_1, self.ancho, self.ala_2, self.grosor, self.longitud, self.ala_3, self.ala_4)
            
            if not referencia_id:
                raise ValidationError(error)
            self.referencia_id = referencia_id    
            self.state = 'REF'
            self.name = self.referencia_id.name
            
            
        if self.type_id.is_solidboard == True:
        
            if not self.ancho or self.ancho <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ancho")
            if not self.grosor or self.grosor <= 0:
                raise ValidationError("Error: Hay que indicar un valor en GROSOR")
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
                
            referencia_id, error = self.type_id.create_prod_solidboard(self.ancho, self.grosor, self.longitud)
            
            if not referencia_id:
                raise ValidationError(error)
            self.referencia_id = referencia_id    
            self.state = 'REF'
            self.name = self.referencia_id.name
            
            
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
            self.state = 'REF'
            self.name = self.referencia_id.name
            
            
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
            self.referencia_id = referencia_id    
            self.state = 'REF'
            self.name = self.referencia_id.name
            
            
        if self.type_id.is_pieballet == True:
        
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
            if not self.pie:
                raise ValidationError("Error: Hay que indicar un valor en PIE")
                
            referencia_id, error = self.type_id.create_prod_pieballet(self.longitud, self.pie)
            
            if not referencia_id:
                raise ValidationError(error)
            self.referencia_id = referencia_id    
            self.state = 'REF'
            self.name = self.referencia_id.name
            
            
        
    @api.multi
    def ref_to_rcl(self):
        self.state = 'RCL'
        
    
        
    @api.multi
    def cancel_offer(self):
        self.state = 'CAN'
    
    
    
    
class sale_product_attribute(models.Model):
    _name = 'sale.product.attribute'

    referencia_cliente_id = fields.Many2one('sale.referencia.cliente', string="Referencia cliente")
    partner_id = fields.Many2one('res.partner', string='Cliente', store=True, related='referencia_cliente_id.partner_id')
    
    name = fields.Char('Nombre', required=True)
    
    color_id = fields.Many2one('product.caracteristica.color', string="Color")
    corte_v = fields.Integer('Corte V')
    redondo = fields.Integer('Redondo')
    especial_id = fields.Many2one('product.caracteristica.especial', string="Especial")
    reciclable_id = fields.Many2one('product.caracteristica.reciclable', string="Reciclable")
    impresion_id = fields.Many2one('product.caracteristica.impresion', string="Impresión")
    texto_impresion = fields.Char("Texto Impresión")
    comentario_producto = fields.Char("Comentario Producto")
    producto_fabricado = fields.Boolean("Producto fabricado")
    
    #OFERTA
    oferta_ids = fields.One2many('sale.offer.oferta', 'attribute_id', string="Ofertas", copy=True)
    
    def get_price(self, num_pallets, state_id, country_id):
        #3p
        #5p
        #8p
        #Si son 12 -> 8p
        #Si son 7 -> 5p
        #Si son 2 -> Error
        
        if self.referencia_cliente_id.state != 'RCL':
            return -1
        
        npal = -1
        precio = -1
        
        for of in self.oferta_ids:
            if state_id == of.state_id and country_id == of.country_id:
                if num_pallets >= of.npallets and of.npallets > npal:
                    npal = of.npallets
                    precio = of.get_valor()
                    
        return precio

    
    
    
    
    
class sale_offer_oferta(models.Model):
    _name = 'sale.offer.oferta'
    
    attribute_id = fields.Many2one('sale.product.attribute', string="Atributo producto", required=True, )
    user_id = fields.Many2one('res.users', string="Comercial", default=lambda self: self.env.user, required=True)
    date = fields.Date('Fecha', default=fields.Date.today(), required=True)
    npallets = fields.Integer('Num pallets')
    emetro = fields.Float('Emetro')
    eton = fields.Float('Eton')
    
    TIPOS = [('EM','€/metro'),   
             ('ET','€/ton'),
            ]
    etipo = fields.Selection(selection=TIPOS, string='Etipo', default='EM')
    state_id = fields.Many2one('res.country.state', string="Provincia")
    country_id = fields.Many2one('res.country', string="País")
    activa = fields.Boolean("Activa")
    enviada = fields.Boolean("Enviada")
    usada = fields.Boolean("Usada")
    
    referencia_cliente_id = fields.Many2one('sale.referencia.cliente', string='Referencia cliente', store=True, related='attribute_id.referencia_cliente_id')
    partner_id = fields.Many2one('res.partner', string='Cliente', store=True, related='attribute_id.referencia_cliente_id.partner_id')
    
    def get_valor(self):
        if self.etipo == "EM":
            return self.emetro
        return self.eton
        
    def name_get(self):
        result = []
        for of in self:
            name = str(of.npallets) + 'P: '
            if of.emetro:
                name = name + str(of.emetro) + ' € / m'
            else:
                name = name + str(of.eton) + ' € / ton'
            result.append((of.id, name))
        return result
    
    
    
    
    
    
    
    
    
    