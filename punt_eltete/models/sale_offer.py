
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

    
class sale_referencia_cliente(models.Model):
    _name = 'sale.referencia.cliente'

    name = fields.Char(string='Ref cliente nombre', required=True, default=lambda self: "/") ##POR DEFERCTO EL TITULO, no el name
    
    
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
    grosor_1 = fields.Float('Grosor 1', digits=(6,1))
    grosor_2 = fields.Float('Grosor 2', digits=(8,2))
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
    
    PALETIZADO_SEL = [('1', 'Compacto (Normal)'),                 
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
    
    und_paquete_cliente = fields.Integer('Und paquete cliente')
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
    
    comentario_referencia = fields.Text('Comentario Referencia', related='referencia_id.comentario', readonly=False)


    
    #CALCULOS
    paletizado = fields.Integer('Paletizado', compute="_get_valores")
    ancho_pallet = fields.Integer('Ancho Pallet', compute="_get_valores")
    und_paquete = fields.Integer('Und Paquete', compute="_get_valores")
    paquetes_fila = fields.Integer('Paquetes Fila', compute="_get_valores")
    alto_fila = fields.Integer('Alto Fila', compute="_get_valores")
    fila_max = fields.Integer('Fila Max', compute="_get_valores")
    fila_buena = fields.Integer('Fila Buena', compute="_get_valores")
    
    
    attribute_ids = fields.One2many('sale.product.attribute', 'referencia_cliente_id', string="Atributos", copy=True)
    #oferta_ids = fields.Many2many('sale.offer.oferta', string="Ofertas de la referencia", compute="_get_ofertas", readonly=True)
    oferta_ids = fields.One2many('sale.offer.oferta', 'referencia_cliente_id', string="Ofertas", readonly=True)
    
    
    
    @api.depends('type_id',)
    def _get_valores(self):
    
        for record in self:
            paletizado = 1
            ancho_pallet = 1200
            und_paquete = 0
            paquetes = 1
            alto_fila = 0
            fila_max = 0
            fila_buena = 0

            if record.referencia_id:
            
                pesoUnd  = record.referencia_id.peso_metro * record.referencia_id.metros_unidad
            
                #Varios
                if record.type_id.is_varios == True:
                    if int(record.ancho_pallet_cliente) > 0:
                        ancho_pallet = int(record.ancho_pallet_cliente)
                    if record.und_paquete_cliente > 0:
                        und_paquete = record.und_paquete_cliente
                    paquetes = 1
                    alto_fila = 10
                    fila_max = 100
                    fila_buena = 1
                #Cantonera
                elif record.type_id.is_cantonera == True:

                    alto_fila = (record.referencia_id.ala_1 + record.referencia_id.ala_2) * 0.7071
                    pesoUnidad = record.referencia_id.peso_metro * record.referencia_id.metros_unidad
                    mediaAlas = (record.referencia_id.ala_1 + record.referencia_id.ala_2) / 2
                    
                    if record.referencia_id.longitud < 250:
                        if int(record.ancho_pallet_cliente) > 0:
                            ancho_pallet = int(record.ancho_pallet_cliente)
                        und_paquete = 4000
                        paquetes = 1
                        fila_max = int(1750 / (4000 * pesoUnidad))
                        fila_buena = int(1000 / (4000 * pesoUnidad)) + 1
                    else:
                        #Calculamos paletizado
                        if record.paletizado_cliente == '2':
                            paletizado = 2
                            if record.und_paquete_cliente > 0:     
                                paletizado = 1
                            elif record.und_pallet_cliente > 0:     
                                paletizado = 1
                        #Calculamos ancho pallet   
                        if paletizado == 2:
                            ancho_pallet = 1150
                        if record.contenedor == True and record.referencia_id.longitud > 2300:
                            ancho_pallet = 1000
                        if record.ancho_pallet_cliente:
                            if int(record.ancho_pallet_cliente) < ancho_pallet:
                                ancho_pallet = int(record.ancho_pallet_cliente)
                        #Unidades / paquete
                        undFilaMax = 0
                        if record.und_paquete_cliente > 0:
                            und_paquete = record.und_paquete_cliente
                            undFilaMax = int((ancho_pallet - 0.7071 * mediaAlas) / (record.referencia_id.grosor_2 * 1.5))
                            paquetes = int(undFilaMax / und_paquete)
                        #Compacto
                        elif paletizado == 1:
                            und_paquete = 25
                            if record.referencia_id.grosor_2 >= 5:
                                und_paquete = 10
                            elif record.referencia_id.grosor_2 >= 4:
                                und_paquete = 20
                            pesoPaquete = und_paquete * pesoUnidad
                            while pesoPaquete > 20:
                                und_paquete = und_paquete - 5
                                pesoPaquete = und_paquete * pesoUnidad
                            undFilaMax = int((ancho_pallet - 0.7071 * mediaAlas) / (record.referencia_id.grosor_2 * 1.5))
                            paquetes = int(undFilaMax / und_paquete)
                        #Columnas
                        elif paletizado == 2:
                            undColumna = int(((ancho_pallet - 10) / 4 - 0.7071 * mediaAlas) / (record.referencia_id.grosor_2 * 1.5))
                            paquetesColumna = 2
                            und_paquete = int(undColumna / paquetesColumna)
                            pesoPaquete = und_paquete * pesoUnidad
                            while pesoPaquete > 20:
                                paquetesColumna = paquetesColumna + 1
                                und_paquete = int(undColumna / paquetesColumna)
                                pesoPaquete = und_paquete * pesoUnidad
                            paquetes = paquetesColumna * 4  
                            
                        #Dobles, Triples
                        repetido = 1
                        if record.referencia_id.longitud == 250:
                            repetido = 4
                        elif record.referencia_id.longitud > 250 and record.referencia_id.longitud <= 350:
                            repetido = 3
                        elif record.referencia_id.longitud > 350 and record.referencia_id.longitud <= 650:
                            repetido = 2
                        paquetes = paquetes * repetido
                        
                        #fila_max por altura
                        altoMax = 1250
                        if record.contenedor == True:
                            altoMax = 1100
                        if record.alto_max_cliente > 0 and record.alto_max_cliente < altoMax:
                            altoMax = record.alto_max_cliente
                        altoMax = altoMax - 150
                        fila_max = int(altoMax / alto_fila)
                
                        #Por peso
                        pesoFila = pesoUnidad * und_paquete * paquetes
                        pesoMax = 1750
                        if record.peso_max_cliente > 0 and record.peso_max_cliente < pesoMax:
                            pesoMax = record.peso_max_cliente
                        pesoMadera = 0
                        if record.referencia_id.longitud < 1500:
                            pesoMadera = 20
                        elif record.referencia_id.longitud < 2000:
                            pesoMadera = 30
                        else:
                            pesoMadera = int(record.referencia_id.longitud / 1000) * 20
                        pesoMax = pesoMax - pesoMadera
                        pesoPallet = fila_max * pesoFila
                        while pesoPallet > pesoMax:
                            fila_max = fila_max - 1
                            pesoPallet = fila_max * pesoFila
                        #Fila buena
                        fila_buena = fila_max
                        if record.referencia_id.longitud < 4500:
                            pesoMax = 1300
                        else:
                            pesoMax = 1500
                        while pesoPallet > pesoMax:
                            fila_buena = fila_buena - 1
                            pesoPallet = fila_buena * pesoFila   
                        
                #Perfil U
                elif record.type_id.is_perfilu == True:
                    if record.ancho_pallet_cliente:
                        ancho_pallet = int(record.ancho_pallet_cliente)
                    paquetes = int(ancho_pallet / (record.referencia_id.ancho + record.referencia_id.grosor_2 * 3))
                    if record.longitud <= 600:
                        paquetes = paquetes * 2
              
                    und_paquete = 2
                    alto_fila = record.referencia_id.ala_1 + record.referencia_id.grosor_2
                    #Fila Max
                    altoMax = 1600
                    if record.contenedor == True:
                        altoMax = 1100
                    if int(record.alto_max_cliente) < altoMax:
                        altoMax = int(record.alto_max_cliente)
                    altoMax = altoMax - 150
                    fila_max = int(altoMax / alto_fila)
                    #Fila buena
                    altoMax = 1250
                    if record.contenedor == True:
                        altoMax = 1100
                    if int(record.alto_max_cliente) < altoMax:
                        altoMax = int(record.alto_max_cliente)
                    altoMax = altoMax - 150
                    fila_buena = int(altoMax / alto_fila)
                    
                #Slip Sheets
                elif record.type_id.is_slipsheet == True:
                    und_paquete = 50
                    ancho = record.referencia_id.ancho + record.referencia_id.ala_1 +  record.referencia_id.ala_2
                    largo = record.referencia_id.longitud + record.referencia_id.ala_3 +  record.referencia_id.ala_4
                    lado1 = 1
                    lado2 = 1
                    if ancho <= 650:
                        lado1 = int(1300 / ancho)
                    if largo <= 650:
                        lado2 = int(1300 / largo)
                    paquetes = lado1 * lado2
                    
                    alto_fila = record.referencia_id.grosor_1 * 50
                    fila_max = int(950 / alto_fila)
                    if record.peso_max_cliente > 0:
                        pesoFila = pesoUnd *  und_paquete * paquetes
                        pesoPallet = pesoFila * fila_max + 20
                        while pesoPallet > record.peso_max_cliente:
                            fila_max = fila_max - 1
                            pesoPallet = pesoFila * fila_max + 20
                    fila_buena = 10
                    if fila_buena > fila_max:
                        fila_buena = fila_max
                    
                #Solid Board
                elif record.type_id.is_solidboard == True:
                    und_paquete = 50
                    lado1 = 1
                    lado2 = 1
                    if record.referencia_id.ancho <= 650:
                        lado1 = int(1300 / record.referencia_id.ancho)
                    if record.referencia_id.longitud <= 650:
                        lado2 = int(1300 / record.referencia_id.longitud)
                    paquetes = lado1 * lado2
                    alto_fila = record.referencia_id.grosor_1 * 50
                    fila_max = int(950 / alto_fila)
                    if record.peso_max_cliente > 0:
                        pesoFila = pesoUnd *  und_paquete * paquetes
                        pesoPallet = pesoFila * fila_max + 20
                        while pesoPallet > record.peso_max_cliente:
                            fila_max = fila_max - 1
                            pesoPallet = pesoFila * fila_max + 20
                    fila_buena = 10
                    if fila_buena > fila_max:
                        fila_buena = fila_max
                    
                #Formato
                elif record.type_id.is_formato == True:
                    und_paquete = 50
                    if record.und_paquete_cliente > 0:
                        und_paquete = record.und_paquete_cliente
                    lado1 = 1
                    lado2 = 1
                    if record.referencia_id.ancho <= 650:
                        lado1 = int(1300 / record.referencia_id.ancho)
                    if record.referencia_id.longitud <= 650:
                        lado2 = int(1300 / record.referencia_id.longitud)
                    paquetes = lado1 * lado2
                    alto_fila = record.referencia_id.gramaje * 1.4 * und_paquete
                    fila_max = int(950 / alto_fila)
                    if record.peso_max_cliente > 0:
                        pesoFila = pesoUnd *  und_paquete * paquetes
                        pesoPallet = pesoFila * fila_max + 20
                        while pesoPallet > record.peso_max_cliente:
                            fila_max = fila_max - 1
                            pesoPallet = pesoFila * fila_max + 20
                    fila_buena = 10
                    if fila_buena > fila_max:
                        fila_buena = fila_max
                #Bobina
                elif record.type_id.is_bobina == True:
                    und_paquete = 1
                    if record.referencia_id.diametro > 650:
                        paquetes = 1
                    else:
                        lado1 = int(1300 / record.referencia_id.diametro)
                        lado2 = int(1100 / record.referencia_id.diametro)
                        paquetes = lado1 * lado2  
                    alto_fila = record.referencia_id.ancho
                    fila_max = int(2400 / alto_fila)
                    if record.contenedor == True:
                        fila_max = int(2000 / alto_fila)
                    if record.peso_max_cliente > 0:
                        pesoFila = pesoUnd *  und_paquete * paquetes
                        pesoPallet = pesoFila * fila_max + 20
                        while pesoPallet > record.peso_max_cliente:
                            fila_max = fila_max - 1
                            pesoPallet = pesoFila * fila_max + 20
                    fila_buena = int(1100 / alto_fila)
                    if fila_buena > fila_max:
                        fila_buena = fila_max
                    
                #Pie de Pallet
                elif record.type_id.is_pieballet == True:
                    und_paquete = 1
                    if record.longitud == 190:
                        paquetes = 65
                    elif record.longitud >= 200 and record.longitud < 350:
                        paquetes = 52
                    elif record.longitud >= 350 and record.longitud < 400:
                        paquetes = 39
                    elif record.longitud >= 400 and record.longitud < 660:
                        paquetes = 26
                    else:
                        paquetes = 13
                        
                    if record.pie == "1" or record.pie == "2":
                        alto_fila = 100
                    elif record.pie == "3" or record.pie == "4":
                        alto_fila = 60
                    
                    fila_max = int(1100 / alto_fila)
                    fila_buena = fila_max
        
        
            record.paletizado = paletizado
            record.ancho_pallet = ancho_pallet
            record.und_paquete = und_paquete
            record.paquetes_fila = paquetes
            record.alto_fila = alto_fila
            record.fila_max = fila_max
            record.fila_buena = fila_buena
    
    
    
    
    
    

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
            if not self.grosor_2 or self.grosor_2 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en GROSOR")
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
                
            referencia_id, error = self.type_id.create_prod_cantonera(self.ala_1, self.ala_2, self.grosor_2, self.longitud)
            
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
            if not self.grosor_2 or self.grosor_2 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en GROSOR")
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
                
            referencia_id, error = self.type_id.create_prod_perfilu(self.ala_1, self.ancho, self.ala_2, self.grosor_2, self.longitud)
            
            if not referencia_id:
                raise ValidationError(error)
            self.referencia_id = referencia_id    
            self.state = 'REF'
            self.name = self.referencia_id.name
            
            
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
            self.state = 'REF'
            self.name = self.referencia_id.name
            
            
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
        if not self.precio_cliente:
            raise ValidationError("Error: Hay que indicar un valor en el campo PRECIO CLIENTE")
        self.state = 'RCL'
        
    
        
    @api.multi
    def cancel_offer(self):
        self.state = 'CAN'
    
    
    
    
class sale_product_attribute(models.Model):
    _name = 'sale.product.attribute'

    referencia_cliente_id = fields.Many2one('sale.referencia.cliente', string="Referencia cliente")
    partner_id = fields.Many2one('res.partner', string='Cliente', store=True, related='referencia_cliente_id.partner_id')
    type_id = fields.Many2one('product.category', string="Tipo de producto", store=True, related='referencia_cliente_id.type_id')
    is_cantonera = fields.Boolean('¿Es Cantonera?', related='type_id.is_cantonera')
    is_perfilu = fields.Boolean('¿Es Perfil U?', related='type_id.is_perfilu')
    is_slipsheet = fields.Boolean('¿Es Slip Sheet?', related='type_id.is_slipsheet')
    is_solidboard = fields.Boolean('¿Es Solid Board?', related='type_id.is_solidboard')
    is_formato = fields.Boolean('¿Es Formato?', related='type_id.is_formato')
    is_bobina = fields.Boolean('¿Es Bobina?', related='type_id.is_bobina')
    is_pieballet = fields.Boolean('¿Es Pie de Ballet?', related='type_id.is_pieballet')
    is_varios = fields.Boolean('¿Es Varios?', related='type_id.is_varios')
    
    name = fields.Char('Nombre', compute = "_get_titulo")
    
    #CANTONERA COLOR
    cantonera_color_id = fields.Many2one('product.caracteristica.cantonera.color', string="Cantonera Color")
    cantonera_forma_id = fields.Many2one('product.caracteristica.cantonera.forma', string="Forma")
    cantonera_especial_id = fields.Many2one('product.caracteristica.cantonera.especial', string="Especial")
    cantonera_impresion_id = fields.Many2one('product.caracteristica.cantonera.impresion', string="Impresión")
    
    #PERFILU
    perfilu_color_id = fields.Many2one('product.caracteristica.perfilu.color', string="Perfil U Color")
    
    #CANTONERA Y PERFILU
    inglete_id = fields.Many2one('product.caracteristica.inglete', string = "Tipo Inglete")
    inglete_num = fields.Integer('Numero de Ingletes')
    inglete_texto = fields.Char('Inglete Descripcion')
    
    #SOLID BOARD
    plancha_color_id = fields.Many2one('product.caracteristica.planchacolor', string = "Color")
    
    #FORMATO Y BOBINA
    papel_calidad_id = fields.Many2one('product.caracteristica.papelcalidad', string = "Papel Calidad")
    
    #SLIPSHEET, SOLIDBOARD Y FORMATO
    troquelado_id = fields.Many2one('product.caracteristica.troquelado', string = "Troquelado")
    
    #TODOS
    codigo_cliente = fields.Char('Codigo Cliente')
    fsc_id = fields.Many2one('product.caracteristica.fsc', string = "FSC")
    reciclable_id = fields.Many2one('product.caracteristica.reciclable', string = "Reciclable")
    description = fields.Text("Descripción")
    
    
    #OCULTOS
    cantonera_1 = fields.Boolean('Cantonera 1', readonly = True, compute = "_get_valores_cantonera")
    cantonera_2 = fields.Boolean('Cantonera 2', readonly = True, compute = "_get_valores_cantonera")
    cantonera_3 = fields.Boolean('Cantonera 3', readonly = True, compute = "_get_valores_cantonera")
    cantonera_4 = fields.Boolean('Cantonera 4', readonly = True, compute = "_get_valores_cantonera")
    
    sierra = fields.Boolean('Sierra', readonly = True, compute = "_get_valores")
    incremento_metro = fields.Float('Incremento Metro', digits = (10,4), readonly = True, compute = "_get_incremento_param")
    incremento_unidad = fields.Float('Incremento Unidad', digits = (10,4), readonly = True, compute = "_get_incremento_param")
    incremento_porcentaje = fields.Float('Incremento Porcentaje', digits = (10,4), readonly = True, compute = "_get_incremento_param")
    incremento_pallet = fields.Float('Incremento Pallet', digits = (10,4), readonly = True, compute = "_get_incremento_param")
    
    fila_max = fields.Integer('Fila Max', readonly = True, compute = "_get_fila_max")
    fila_buena = fields.Integer('Fila Buena', readonly = True, compute = "_get_valores")
    
    
    
    #OFERTA
    oferta_ids = fields.One2many('sale.offer.oferta', 'attribute_id', string="Ofertas", copy=True)
    
    
    @api.depends('type_id',)
    def _get_titulo(self):
        for record in self:
            nombre = ''
            
            if record.fsc_id:
                nombre = nombre + record.fsc_id.name + ", "
            if record.reciclable_id:
                nombre = nombre + record.reciclable_id.name + ", "


            if record.referencia_cliente_id:
                #Varios
                if record.type_id.is_varios == True:
                    nombre = nombre
                    
                #Cantonera
                elif record.type_id.is_cantonera == True:
                    if record.cantonera_color_id:
                        nombre = nombre + record.cantonera_color_id.name + ", "
                    if record.cantonera_forma_id:
                        nombre = nombre + record.cantonera_forma_id.name + ", "
                    if record.cantonera_especial_id:
                        nombre = nombre + record.cantonera_especial_id.name + ", "
                    if record.cantonera_impresion_id:
                        nombre = nombre + record.cantonera_impresion_id.name + ", "
                    if record.inglete_num > 0 and record.inglete_id:
                        nombre = nombre + str(record.inglete_num) + " " + record.inglete_id.name + ", "
                    
                #Perfil U
                elif record.type_id.is_perfilu == True:
                    if record.perfilu_color_id:
                        nombre = nombre + record.perfilu_color_id.name + ", "
                    if record.inglete_num > 0 and record.inglete_id:
                        nombre = nombre + str(record.inglete_num) + " " + record.inglete_id.name + ", "
                    
                #Slip Sheets
                elif record.type_id.is_slipsheet == True:
                    if record.troquelado_id:
                        nombre = nombre + record.troquelado_id.name + ", "
                    
                #Solid Board
                elif record.type_id.is_solidboard == True:
                    if record.plancha_color_id:
                        nombre = nombre + record.plancha_color_id.name + ", "
                    if record.troquelado_id:
                        nombre = nombre + record.troquelado_id.name + ", "
                    
                #Formato
                elif record.type_id.is_formato == True:
                    if record.papel_calidad_id:
                        nombre = nombre + record.papel_calidad_id.name + ", "
                    if record.troquelado_id:
                        nombre = nombre + record.troquelado_id.name + ", "
                    
                #Bobina
                elif record.type_id.is_bobina == True:
                    if record.papel_calidad_id:
                        nombre = nombre + record.papel_calidad_id.name + ", "
                    if record.troquelado_id:
                        nombre = nombre + record.troquelado_id.name + ", "
                    
                    
                #Pie de Pallet
                elif record.type_id.is_pieballet == True:
                    if record.papel_calidad_id:
                        nombre = nombre + record.papel_calidad_id.name + ", "
            
            if len(nombre) > 2:
                nombre = nombre[:-2]

            if nombre == '':
                nombre = 'Ninguno'
            record.name = nombre
    


    def _get_incremento(self, num):
        for record in self:
            incremento = 0
            if record.referencia_cliente_id.pallet_especial_id != None and record.referencia_cliente_id.pallet_especial_id.tipo == "1":
                incremento = incremento + record.referencia_cliente_id.pallet_especial_id.incremento
            if record.fsc_id != None and record.fsc_id.tipo == num:
                incremento = incremento + record.fsc_id.incremento
            if record.reciclable_id != None and record.reciclable_id.tipo == num:
                incremento = incremento + record.reciclable_id.incremento
            if record.cantonera_color_id != None and record.cantonera_color_id.tipo == num:
                incremento = incremento + record.cantonera_color_id.incremento
            if record.cantonera_forma_id != None and record.cantonera_forma_id.tipo == num:
                incremento = incremento + record.cantonera_forma_id.incremento
            if record.cantonera_especial_id != None and record.cantonera_especial_id.tipo == num:
                incremento = incremento + record.cantonera_especial_id.incremento
            if record.cantonera_impresion_id != None and record.cantonera_impresion_id.tipo == num:
                incremento = incremento + record.cantonera_impresion_id.incremento
            if record.perfilu_color_id != None and record.perfilu_color_id.tipo == num:
                incremento = incremento + record.perfilu_color_id.incremento
            if record.inglete_id != None and record.inglete_num > 0 and record.inglete_id.tipo == num:
                incremento = incremento + record.inglete_id.incremento * record.inglete_num
            if record.plancha_color_id != None and record.plancha_color_id.tipo == num:
                incremento = incremento + record.plancha_color_id.incremento
            if record.papel_calidad_id != None and record.papel_calidad_id.tipo == num:
                incremento = incremento + record.papel_calidad_id.incremento
            if record.troquelado_id != None and record.troquelado_id.tipo == num:
                incremento = incremento + record.troquelado_id.incremento
            return incremento
            
        
    @api.depends('type_id',)
    def _get_incremento_param(self):
        for record in self:
            record.incremento_metro = record._get_incremento("1")
            record.incremento_unidad = record._get_incremento("2")
            record.incremento_porcentaje = record._get_incremento("3")
            record.incremento_pallet = record._get_incremento("4")


        

    
    @api.depends('type_id',)
    def _get_fila_max(self):
    
        for record in self:
    
            filaMax = 0
            undFila = record.referencia_cliente_id.und_paquete * record.referencia_cliente_id.paquetes_fila
            pesoUnidad = record.referencia_cliente_id.referencia_id.peso_metro * record.referencia_cliente_id.referencia_id.metros_unidad
            pesoFila = pesoUnidad * record.referencia_cliente_id.und_paquete * record.referencia_cliente_id.paquetes_fila
            
            #Unidades exactas
            if record.referencia_cliente_id.und_pallet_cliente and record.referencia_cliente_id.und_pallet_cliente > 0:
                if undFila != 0:
                    filaMax = int(record.referencia_cliente_id.und_pallet_cliente / undFila)
                    if filaMax * undFila < record.referencia_cliente_id.und_pallet_cliente:
                        filaMax = filaMax + 1    
            #Varios
            elif record.type_id.is_varios == True:
                if pesoFila != 0:
                    filaMax = int(1750 / pesoFila)
            #Cantonera
            elif record.type_id.is_cantonera == True and record.referencia_cliente_id.referencia_id.longitud < 250:
                if pesoFila != 0:
                    filaMax = int(1750 / pesoFila)
            #Perfil U
            elif record.type_id.is_perfilu == True and record.referencia_cliente_id.referencia_id.longitud < 250:
                if pesoFila != 0:
                    filaMax = int(1750 / pesoFila)
                
            else:
                altoMax = 1600
                if record.referencia_cliente_id.contenedor == True:
                    altoMax = 1100
                elif record.type_id.is_slipsheet == True:
                    altoMax = 1100
                elif record.type_id.is_solidboard == True:
                    altoMax = 1100
                elif record.type_id.is_formato == True:
                    altoMax = 1100
                elif record.type_id.is_bobina == True:
                    altoMax = 2200
                elif record.type_id.is_pieballet == True:
                    altoMax = 1250
                        
                if record.referencia_cliente_id.alto_max_cliente < altoMax:
                    altoMax = record.referencia_cliente_id.und_pallet_cliente    
                filaMax = int((altoMax - 150) / record.referencia_cliente_id.alto_fila)
                
                #Por peso
                pesoPallet = pesoFila * filaMax
                pesoMadera = 0
                if record.referencia_cliente_id.referencia_id.longitud < 1500:
                    pesoMadera = 20
                elif record.referencia_cliente_id.referencia_id.longitud < 2000:
                    pesoMadera = 30
                else:
                    pesoMadera = int(record.referencia_cliente_id.referencia_id.longitud / 1000) * 20
                        
                pesoMax = 1750 - pesoMadera        
                if record.referencia_cliente_id.peso_max_cliente and record.referencia_cliente_id.peso_max_cliente > 0:
                    if record.referencia_cliente_id.peso_max_cliente < pesoMax:
                        pesoMax = record.referencia_cliente_id.peso_max_cliente
                while pesoPallet > pesoMax:
                    filaMax = filaMax - 1
                    pesoPallet = pesoFila * filaMax
        
            record.fila_max = filaMax
    
    @api.depends('type_id',)
    def _get_valores(self):
        for record in self:
            sierra = False
            
            buena = 0
            if record.referencia_cliente_id.und_pallet_cliente != None and record.referencia_cliente_id.und_pallet_cliente > 0:
                buena = record.fila_max

            if record.referencia_cliente_id:
                #Varios
                if record.type_id.is_varios == True:
                    sierra = False
                    
                #Cantonera
                elif record.type_id.is_cantonera == True:
                    if record.referencia_cliente_id.longitud < 500:
                        sierra = True
                        
                    undFila = record.referencia_cliente_id.und_paquete * record.referencia_cliente_id.paquetes_fila
                    pesoUnidad = record.referencia_cliente_id.referencia_id.peso_metro * record.referencia_cliente_id.referencia_id.metros_unidad
                    pesoFila = pesoUnidad * record.referencia_cliente_id.und_paquete * record.referencia_cliente_id.paquetes_fila
                    buena = record.fila_max
                    #Por peso
                    pesoMax = 1500
                    if record.referencia_cliente_id.referencia_id.longitud <= 4500:
                        pesoMax = 1300
                    pesoPallet = pesoFila * buena
                    while pesoPallet > pesoMax:
                        buena = buena - 1
                        pesoPallet = pesoFila * buena
                    #Repetido
                    repetido = 1
                    if record.referencia_cliente_id.referencia_id.longitud == 250:
                        repetido = 4
                    elif record.referencia_cliente_id.referencia_id.longitud > 250 and record.referencia_cliente_id.referencia_id.longitud <= 350:
                        repetido = 3
                    elif record.referencia_cliente_id.referencia_id.longitud > 350 and record.referencia_cliente_id.referencia_id.longitud <= 650:
                        repetido = 2    
                    while undFila * buena / repetido > 7000:
                        buena = buena - 1
                    
                #Perfil U
                elif record.type_id.is_perfilu == True:
                    if record.referencia_cliente_id.longitud < 400:
                        sierra = True
                        
                    buena = record.fila_max
                    
                #Slip Sheets
                elif record.type_id.is_slipsheet == True:
                    buena = 10
                    
                #Solid Board
                elif record.type_id.is_solidboard == True:
                    buena = 10
                    
                #Formato
                elif record.type_id.is_formato == True:
                    buena = record.fila_max
                    pesoMax = 1300
                    pesoUnidad = record.referencia_cliente_id.referencia_id.peso_metro * record.referencia_cliente_id.referencia_id.metros_unidad
                    pesoFila = pesoUnidad * record.referencia_cliente_id.und_paquete * record.referencia_cliente_id.paquetes_fila
                    pesoPallet = pesoFila * buena
                    while pesoPallet > pesoMax:
                        buena = buena - 1
                        pesoPallet = pesoFila * buena
                    
                #Bobina
                elif record.type_id.is_bobina == True:
                    buena = record.fila_max
                    pesoMax = 1300
                    pesoUnidad = record.referencia_cliente_id.referencia_id.peso_metro * record.referencia_cliente_id.referencia_id.metros_unidad
                    pesoFila = pesoUnidad * record.referencia_cliente_id.und_paquete * record.referencia_cliente_id.paquetes_fila
                    pesoPallet = pesoFila * buena
                    while pesoPallet > pesoMax:
                        buena = buena - 1
                        pesoPallet = pesoFila * buena
                    
                    
                #Pie de Pallet
                elif record.type_id.is_pieballet == True:
                    buena = record.fila_max
            

            record.sierra = sierra
            record.fila_buena = buena
    
    
    
    
    
    @api.depends('referencia_cliente_id',)
    def _get_valores_cantonera(self):
        for record in self:
            if record.referencia_cliente_id:
                if record.type_id.is_cantonera == True:
                
                    
                    habilitado = True
                    if record.fsc_id and record.fsc_id.cantonera_1 == False:
                        habilitado = False
                    elif record.reciclable_id and record.reciclable_id.cantonera_1 == False:
                        habilitado = False
                    elif record.cantonera_forma_id and record.cantonera_forma_id.cantonera_1 == False:
                        habilitado = False
                    elif record.cantonera_especial_id and record.cantonera_especial_id.cantonera_1 == False:
                        habilitado = False
                    elif record.cantonera_impresion_id and record.cantonera_impresion_id.cantonera_1 == False:
                        habilitado = False
                    record.cantonera_1 = habilitado
                
                    habilitado = True
                    if record.referencia_cliente_id.referencia_id.ala_1 > 60:
                        habilitado = False
                    elif record.referencia_cliente_id.referencia_id.ala_2 > 60:
                        habilitado = False
                    elif record.referencia_cliente_id.referencia_id.grosor_2 > 5:
                        habilitado = False
                    elif record.fsc_id and record.fsc_id.cantonera_2 == False:
                        habilitado = False
                    elif record.reciclable_id and record.reciclable_id.cantonera_2 == False:
                        habilitado = False
                    elif record.cantonera_forma_id and record.cantonera_forma_id.cantonera_2 == False:
                        habilitado = False
                    elif record.cantonera_especial_id and record.cantonera_especial_id.cantonera_2 == False:
                        habilitado = False
                    elif record.cantonera_impresion_id and record.cantonera_impresion_id.cantonera_2 == False:
                        habilitado = False
                    record.cantonera_2 = habilitado
                    
                    habilitado = True
                    if record.referencia_cliente_id.referencia_id.ala_1 > 50:
                        habilitado = False
                    elif record.referencia_cliente_id.referencia_id.ala_2 > 50:
                        habilitado = False
                    elif record.referencia_cliente_id.referencia_id.grosor_2 > 4.5:
                        habilitado = False
                    elif record.fsc_id and record.fsc_id.cantonera_3 == False:
                        habilitado = False
                    elif record.reciclable_id and record.reciclable_id.cantonera_3 == False:
                        habilitado = False
                    elif record.cantonera_forma_id and record.cantonera_forma_id.cantonera_3 == False:
                        habilitado = False
                    elif record.cantonera_especial_id and record.cantonera_especial_id.cantonera_3 == False:
                        habilitado = False
                    elif record.cantonera_impresion_id and record.cantonera_impresion_id.cantonera_3 == False:
                        habilitado = False
                    record.cantonera_3 = habilitado
                    
                    habilitado = True
                    if record.fsc_id and record.fsc_id.cantonera_4 == False:
                        habilitado = False
                    elif record.reciclable_id and record.reciclable_id.cantonera_4 == False:
                        habilitado = False
                    elif record.cantonera_forma_id and record.cantonera_forma_id.cantonera_4 == False:
                        habilitado = False
                    elif record.cantonera_especial_id and record.cantonera_especial_id.cantonera_4 == False:
                        habilitado = False
                    elif record.cantonera_impresion_id and record.cantonera_impresion_id.cantonera_4 == False:
                        habilitado = False
                        
                    record.cantonera_4 = habilitado
    
    
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
                if num_pallets >= of.num_pallets and of.num_pallets > npal:
                    npal = of.npallets
                    precio = of.get_valor()
                    
        return precio

    
    
    
    
    
class sale_offer_oferta(models.Model):
    _name = 'sale.offer.oferta'
    
    attribute_id = fields.Many2one('sale.product.attribute', string="Atributo producto", required=True, )
    user_id = fields.Many2one('res.users', string="Comercial", default=lambda self: self.env.user, required=True)
    referencia_cliente_id = fields.Many2one('sale.referencia.cliente', string='Referencia cliente', store=True, related='attribute_id.referencia_cliente_id')
    partner_id = fields.Many2one('res.partner', string='Cliente', store=True, related='attribute_id.referencia_cliente_id.partner_id')
    date = fields.Date('Fecha', default=fields.Date.today(), required=True)
    
    num_pallets = fields.Integer('Num pallets')
    emetro_user = fields.Float('Emetro (user)')
    eton_user = fields.Float('Eton (user)')
    tarifa = fields.Boolean('Tarifa', default = True)
    
    state_id = fields.Many2one('res.country.state', string="Provincia")
    country_id = fields.Many2one('res.country', string="País")
    activa = fields.Boolean("Activa")
    
    #CALCULADOS
    num_filas = fields.Integer('Num filas', readonly = True)
    und_pallet = fields.Integer('Unidades', readonly = True, compute = "_get_und_pallet")
    peso_neto = fields.Integer('Peso Neto', readonly = True, compute = "_get_peso_neto")
    peso_bruto = fields.Integer('Peso Bruto', readonly = True, compute = "_get_peso_bruto")
    alto_pallet = fields.Integer('Alto', readonly = True, compute = "_get_alto_pallet")
    
    emetro = fields.Float('Emetro', readonly = True, digits = (10,4), compute = "_get_emetro")
    eton = fields.Float('Eton', readonly = True, digits = (8,1), compute = "_get_eton")
    titulo = fields.Char('Título', readonly = True, compute = "_get_titulo")
    name = fields.Char('Precio', readonly = True, compute = "_get_precio")
    

        
    @api.multi
    def suma_filas(self):
        if self.attribute_id.referencia_cliente_id.und_pallet_cliente > 0:
            x = 0
        elif self.num_filas < self.attribute_id.referencia_cliente_id.fila_max:
            self.num_filas = self.num_filas + 1
            
    @api.multi
    def resta_filas(self):
        if self.attribute_id.referencia_cliente_id.und_pallet_cliente > 0:
            x = 0
        elif self.num_filas > 1:
            self.num_filas = self.num_filas - 1
    
    

    
    
    @api.depends('attribute_id',)
    def _get_und_pallet(self):
        for record in self:
            und = 0
            if record.attribute_id.referencia_cliente_id.und_pallet_cliente > 0:
                und = record.attribute_id.referencia_cliente_id.und_pallet_cliente
            else:
                undFila = record.attribute_id.referencia_cliente_id.und_paquete * record.attribute_id.referencia_cliente_id.paquetes_fila
                und = undFila * record.num_filas
                
            record.und_pallet = und
    
    
    @api.depends('attribute_id', 'emetro_user', 'eton_user', 'num_pallets')
    def _get_peso_neto(self):
        und = self.und_pallet
        pesoUnd = self.attribute_id.referencia_cliente_id.referencia_id.peso_metro * self.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
        peso = und * pesoUnd
        self.peso_neto = peso
    
    
    @api.depends('attribute_id', 'emetro_user', 'eton_user', 'num_pallets')
    def _get_peso_bruto(self):
        peso = self.peso_neto
        pesoMadera = 0
        if self.attribute_id.referencia_cliente_id.referencia_id.longitud < 1500:
            pesoMadera = 20
        elif self.attribute_id.referencia_cliente_id.referencia_id.longitud < 2000:
            pesoMadera = 30
        else:
            pesoMadera = int(self.attribute_id.referencia_cliente_id.referencia_id.longitud / 1000) * 20
        peso = peso + pesoMadera
        return peso
        
        
    @api.depends('attribute_id', 'emetro_user', 'eton_user', 'num_pallets')
    def _get_alto_pallet(self):
        for record in self:
            record.alto_pallet = record.attribute_id.referencia_cliente_id.alto_fila * record.num_filas + 150
        
        
    @api.depends('attribute_id', 'emetro_user', 'eton_user', 'num_pallets')
    def _get_emetro(self):
        for record in self:
            valor = 0
            if record.emetro_user > 0:
                valor = record.emetro_user
            elif record.eton_user > 0:
                valor = record.metroPorTon()
            record.emetro = valor
        
        
    def metroPorTon(self):
        valor = 0
        if self.tarifa == True:
            valor = self.eton_user * self.attribute_id.referencia_cliente_id.referencia_id.peso_metro / 1000
            valor = valor * (self.attribute_id.incremento_porcentaje / 100 + 1)
            valor = valor + self.attribute_id.incremento_metro
            valor = valor * self.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
            valor = valor + self.attribute_id.incremento_unidad
            if self.attribute_id.sierra == True:
                valor = valor + 0.017
            if self.und_pallet != 0:
                valor = valor + self.attribute_id.incremento_pallet / self.und_pallet
            valor = valor / self.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
            valor = int(valor * 1000) / 1000
        else:
            valor = self.eton_user * self.attribute_id.referencia_cliente_id.referencia_id.peso_metro / 1000
            valor = valor * self.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
            if self.attribute_id.sierra == True:
                valor = valor + 0.017
            valor = valor / self.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
            valor = int(valor * 1000) / 1000
        return valor
    
    
    @api.depends('attribute_id', 'emetro_user', 'eton_user', 'num_pallets')
    def _get_eton(self):
        for record in self:
            valor = 0
            if record.emetro_user > 0:
                if record.attribute_id.referencia_cliente_id.referencia_id.peso_metro != 0:
                    valor = record.emetro_user * 1000 / record.attribute_id.referencia_cliente_id.referencia_id.peso_metro
                    valor = int(valor * 10) / 10
            elif record.eton_user > 0:
                valor = record.eton_user
            record.eton = valor
    
    
    
    @api.depends('attribute_id', 'emetro_user', 'eton_user', 'num_pallets')
    def _get_titulo(self):
        for record in self:
            record.titulo = str(record.und_pallet) + ", " + str(round(record.eton,2)) + " €/t"
    
    
    @api.depends('attribute_id', 'emetro_user', 'eton_user', 'num_pallets')
    def _get_precio(self):
        for record in self:
            texto = ""
            facturar = record.attribute_id.referencia_cliente_id.precio_cliente
            if record.emetro_user > 0 and facturar != '4':
                #Metro
                if facturar == '1':
                    texto = str(record.emetro_user) + " €/metro"
                #Unidad
                elif facturar == '2':
                    aux = str(record.emetro_user * record.attribute_id.referencia_cliente_id.referencia_id.metros_unidad)
                    texto = aux + " €/unidad"
                #Millar
                elif facturar == '3':
                    aux = str(record.emetro_user * record.attribute_id.referencia_cliente_id.referencia_id.metros_unidad * 1000)
                    texto = aux + " €/millar"
                    
            elif record.eton_user != None and record.eton_user > 0:
                valor = record.metroPorTon()
                #Metro
                if facturar == '1':
                    texto = str(valor) + " €/metro"
                #Unidad
                elif facturar == '2':
                    aux = str(valor * record.attribute_id.referencia_cliente_id.referencia_id.metros_unidad)
                    texto = aux + " €/unidad"
                #Millar
                elif facturar == '3':
                    aux = str(valor * record.attribute_id.referencia_cliente_id.referencia_id.metros_unidad * 1000)
                    texto = aux + " €/millar"
                #Kilos
                elif facturar == '4':
                    aux = str(record.eton_user / 1000)
                    texto = aux + " €/kg"
            record.name = texto