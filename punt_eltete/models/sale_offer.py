
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

    
class sale_referencia_cliente(models.Model):
    _name = 'sale.referencia.cliente'

    name = fields.Char(string='Título', compute="_get_name", store=True) ##POR DEFERCTO EL TITULO, no el name
    referencia_cliente_nombre = fields.Char(string='Ref cliente nombre')
    
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
    is_flatboard = fields.Boolean('¿Es Flat Board?', related='type_id.is_flatboard')
    is_mprima_papel = fields.Boolean('¿Es mPrima Papel?', related='type_id.is_mprima_papel')
    
    TIPO_PIE = [('1', 'Alto 100 con Adhesivo'), 
               ('2', 'Alto 100 sin Adhesivo'),
               ('3', 'Alto 60 con Adhesivo'),                 
               ('4', 'Alto 60 sin Adhesivo'),         #La coma final?
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
    tipo_varios_id = fields.Many2one('product.caracteristica.varios', string="Tipo varios",)

    ancho_interior = fields.Integer('Ancho Interior')
    ancho_superficie = fields.Integer('Ancho Superficie')

    referencia_id = fields.Many2one('product.referencia', string="Referencia", readonly = True)

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
    
    und_paquete_cliente = fields.Integer('Und paquete cliente', default = -1)
    und_pallet_cliente = fields.Integer('Unidades Exactas', default = -1)
    alto_max_cliente = fields.Integer('Alto máximo cliente', default = -1)
    peso_max_cliente = fields.Integer('Peso máximo cliente', default = -1)
    
    comentario_paletizado = fields.Text('Comentario Paletizado')
    PRECIO_SEL = [('1', 'metro / metro2'),     
                  ('2', 'unidad'),
                  ('3', 'millar'),
                  ('4', 'kilos'), 
                  ('5', 'varios unidad'), 
                  ]
    precio_cliente = fields.Selection(selection = PRECIO_SEL, string = 'Facturar por:', required=True)
    
    comentario_referencia = fields.Text('Comentario común', related='referencia_id.comentario', readonly=False)

    #CALCULOS
    ocultar = fields.Boolean('Ocultar datos', default = True)
    paletizado = fields.Integer('Paletizado', compute="_get_valores")
    ancho_pallet = fields.Integer('Ancho Pallet', compute="_get_valores")
    und_paquete = fields.Integer('Und Paquete', compute="_get_valores")
    paquetes_fila = fields.Integer('Paquetes Fila', compute="_get_valores")
    alto_fila = fields.Integer('Alto Fila', compute="_get_valores")
    fila_max = fields.Integer('Fila Max', compute="_get_valores")
    fila_buena = fields.Integer('Fila Buena', compute="_get_valores")
    
    
    attribute_ids = fields.One2many('sale.product.attribute', 'referencia_cliente_id', string="Atributos", copy=True)
    oferta_ids = fields.One2many('sale.offer.oferta', 'referencia_cliente_id', string="Ofertas", copy=True)
     
    
    
    @api.depends('type_id', 'referencia_id', 'referencia_cliente_nombre')
    def _get_name(self):
    
        for record in self:
            titulo = ''
            if record.referencia_id.titulo:
                titulo = record.referencia_id.titulo
            type_id_name = ''
            if record.type_id:
                type_id_name = record.type_id.name
            referencia_cliente_nombre = ''
            if record.referencia_cliente_nombre:
                referencia_cliente_nombre = record.referencia_cliente_nombre
            if referencia_cliente_nombre != titulo:
                record.name = type_id_name + " - " + referencia_cliente_nombre + " (" + titulo + ")" 
            else:
                record.name = type_id_name + " - " + titulo
    
    
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
            
                #Cantonera
                if record.type_id.is_cantonera == True:

                    alto_fila = (record.referencia_id.ala_1 + record.referencia_id.ala_2) * 0.7071
                    pesoUnidad = record.referencia_id.peso_metro * record.referencia_id.metros_unidad
                    mediaAlas = (record.referencia_id.ala_1 + record.referencia_id.ala_2) / 2
                    
                    if record.referencia_id.longitud < 200:
                        if int(record.ancho_pallet_cliente) > 0:
                            ancho_pallet = int(record.ancho_pallet_cliente)
                        und_paquete = 4000
                        paquetes = 1
                        fila_max = int(2000 / (4000 * pesoUnidad))
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
                            if record.referencia_id.grosor_2 >= 6:
                                und_paquete = 10
                            elif record.referencia_id.grosor_2 >= 5:
                                und_paquete = 15
                            elif record.referencia_id.grosor_2 >= 4:
                                und_paquete = 20
                            pesoPaquete = und_paquete * pesoUnidad
                            while pesoPaquete > 20:
                                und_paquete = und_paquete - 5
                                pesoPaquete = und_paquete * pesoUnidad
                            undFilaMax = int( ((ancho_pallet - 0) - 0.7071 * mediaAlas) / (record.referencia_id.grosor_2 * 1.5))
                            paquetes = int(undFilaMax / und_paquete)
                            if paquetes > 14:
                                paquetes = paquetes - 1
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
                        if record.referencia_id.longitud == 200:
                            repetido = 5
                        elif record.referencia_id.longitud <= 250:
                            repetido = 4
                        elif record.referencia_id.longitud > 250 and record.referencia_id.longitud <= 350:
                            repetido = 3
                        elif record.referencia_id.longitud > 350 and record.referencia_id.longitud <= 650:
                            repetido = 2
                        paquetes = paquetes * repetido
                        
                        #Unidades Exactas
                        if record.und_pallet_cliente > 0:
                            fila_max = int(record.und_pallet_cliente / (und_paquete * paquetes))
                            if fila_max * und_paquete * paquetes < record.und_pallet_cliente:
                                fila_max = fila_max + 1
                            fila_buena = fila_max
                        
                        #fila_max por altura
                        altoMax = 1600
                        if record.contenedor == True:
                            altoMax = 1100
                        if record.alto_max_cliente > 0 and record.alto_max_cliente < altoMax:
                            altoMax = record.alto_max_cliente
                        altoMax = altoMax - 150
                        fila_max = int(altoMax / alto_fila)
                
                        #Por peso
                        pesoFila = pesoUnidad * und_paquete * paquetes
                        pesoMax = 2000
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
                        altoMax = 1250
                        if record.contenedor == True:
                            altoMax = 1100
                        if record.alto_max_cliente > 0 and record.alto_max_cliente < altoMax:
                            altoMax = record.alto_max_cliente
                        altoMax = altoMax - 150
                        fila_buena = int(altoMax / alto_fila)
                        #Por peso
                        pesoMax = 1500
                        if record.referencia_id.longitud < 4500:
                            pesoMax = 1300
                        pesoPallet = fila_buena * pesoFila
                        while pesoPallet > pesoMax:
                            fila_buena = fila_buena - 1
                            pesoPallet = fila_buena * pesoFila
                        #Por unidades
                        undPalletFila = fila_buena * und_paquete * paquetes / repetido
                        while undPalletFila > 7000:
                            fila_buena = fila_buena - 1
                            undPalletFila = fila_buena * und_paquete * paquetes / repetido
                        
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
                    if record.alto_max_cliente > 0 and record.alto_max_cliente < altoMax:
                        altoMax = int(record.alto_max_cliente)
                    altoMax = altoMax - 150
                    fila_max = int(altoMax / alto_fila)
                    #Fila buena
                    altoMax = 1250
                    if record.contenedor == True:
                        altoMax = 1100
                    if record.alto_max_cliente > 0 and record.alto_max_cliente < altoMax:
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
                    medida_larga = record.referencia_id.longitud
                    medida_corta = record.referencia_id.ancho
                    if medida_corta > medida_larga:
                        medida_larga = record.referencia_id.ancho
                        medida_corta = record.referencia_id.longitud
                    if medida_larga > 1200:
                        lado1 = 1
                        lado2 = int(1200 / medida_corta)
                    elif medida_larga > 1000:
                        lado1 = 1
                        lado2 = int(1000 / medida_corta)
                    else:
                        lado1 = int(1000 / medida_larga)
                        lado2 = int(1200 / medida_corta)
                    if lado1 < 0:
                        lado1 = 1
                    if lado2 < 0:
                        lado2 = 1
                    paquetes = lado1 * lado2
                    alto_fila = record.referencia_id.gramaje * 1.4 * und_paquete / 1000
                    fila_max = int(950 / alto_fila)
                    if record.peso_max_cliente > 0:
                        pesoFila = pesoUnd *  und_paquete * paquetes
                        pesoPallet = pesoFila * fila_max + 20
                        while pesoPallet > record.peso_max_cliente:
                            fila_max = fila_max - 1
                            pesoPallet = pesoFila * fila_max + 20
                    fila_buena = fila_max
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
                        
                    if record.pie == "1":
                        alto_fila = 100
                    elif record.pie == "2":
                        alto_fila = 60
                    
                    fila_max = int(1100 / alto_fila)
                    fila_buena = fila_max
                    
                #Flat Board
                elif record.type_id.is_flatboard == True:
                    if record.ancho_pallet_cliente:
                        ancho_pallet = int(record.ancho_pallet_cliente)
                    paquetes = int(ancho_pallet / record.referencia_id.ancho)
                    if record.longitud <= 600:
                        paquetes = paquetes * 2
              
                    und_paquete = 1
                    alto_fila = record.referencia_id.grosor_1
                    #Fila Max
                    altoMax = 1600
                    if record.contenedor == True:
                        altoMax = 1100
                    if record.alto_max_cliente > 0 and record.alto_max_cliente < altoMax:
                        altoMax = int(record.alto_max_cliente)
                    altoMax = altoMax - 150
                    fila_max = int(altoMax / alto_fila)
                    #Fila buena
                    altoMax = 1250
                    if record.contenedor == True:
                        altoMax = 1100
                    if record.alto_max_cliente > 0 and record.alto_max_cliente < altoMax:
                        altoMax = int(record.alto_max_cliente)
                    altoMax = altoMax - 150
                    fila_buena = int(altoMax / alto_fila)
                    
        
        
            record.paletizado = paletizado
            record.ancho_pallet = ancho_pallet
            record.und_paquete = und_paquete
            record.paquetes_fila = paquetes
            record.alto_fila = alto_fila
            record.fila_max = fila_max
            record.fila_buena = fila_buena
    
    
    
    @api.multi
    def ocultar_datos(self):
        if self.ocultar == True:
            self.ocultar = False
        else:
            self.ocultar = True
        
    
    

    @api.depends('attribute_ids',)
    def _get_ofertas(self):
        lista_ids = []
        for att in self.attribute_ids:
            lista_ids.append(att.id)
        self.oferta_ids = self.env['sale.offer.oferta'].search([('attribuite_id', 'in', lista_ids)])

    
    
    @api.multi
    def bor_to_rcl(self):
        self.bor_to_ref()
        self.ref_to_rcl()
    
    
    
    def check_duplicado_referencia(self, referencia_id):
        if len(self.env['sale.referencia.cliente'].search([('partner_id', '=', self.partner_id.id), ('referencia_id', '=', referencia_id.id)])) > 0:
            return True
        return False
    
    
    @api.multi
    def bor_to_ref(self):
    
        if self.type_id.is_varios == True:

            if not self.tipo_varios_id:
                raise ValidationError("Error: Hay que indicar un valor de Varios")

            referencia_id, error = self.type_id.create_prod_varios(self.tipo_varios_id)

            if not referencia_id:
                raise ValidationError(error)

            if self.check_duplicado_referencia(referencia_id):
                raise ValidationError("Error: Este cliente ya tiene esta referencia creada")

            self.referencia_id = referencia_id    
            self.state = 'REF'
            self.referencia_cliente_nombre = self.referencia_id.titulo
            
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
                
            if self.check_duplicado_referencia(referencia_id):
                raise ValidationError("Error: Este cliente ya tiene esta referencia creada")
                
            self.referencia_id = referencia_id    
            self.state = 'REF'
            self.referencia_cliente_nombre = self.referencia_id.titulo
            
            
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
                
            if self.check_duplicado_referencia(referencia_id):
                raise ValidationError("Error: Este cliente ya tiene esta referencia creada")
                
            self.referencia_id = referencia_id    
            self.state = 'REF'
            self.referencia_cliente_nombre = self.referencia_id.titulo
            
            
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
                
            if self.check_duplicado_referencia(referencia_id):
                raise ValidationError("Error: Este cliente ya tiene esta referencia creada")
                
            self.referencia_id = referencia_id    
            self.state = 'REF'
            self.referencia_cliente_nombre = self.referencia_id.titulo
            
            
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
                
            if self.check_duplicado_referencia(referencia_id):
                raise ValidationError("Error: Este cliente ya tiene esta referencia creada")
                
            self.referencia_id = referencia_id    
            self.state = 'REF'
            self.referencia_cliente_nombre = self.referencia_id.titulo
            
            
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
                
            if self.check_duplicado_referencia(referencia_id):
                raise ValidationError("Error: Este cliente ya tiene esta referencia creada")
                
            self.referencia_id = referencia_id    
            self.state = 'REF'
            self.referencia_cliente_nombre = self.referencia_id.titulo
            
            
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
            self.state = 'REF'
            self.referencia_cliente_nombre = self.referencia_id.titulo
            
            
        if self.type_id.is_pieballet == True:
        
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
            if not self.pie:
                raise ValidationError("Error: Hay que indicar un valor en PIE")
                
            referencia_id, error = self.type_id.create_prod_pieballet(self.longitud, self.pie)
            
            
            
            if not referencia_id:
                raise ValidationError(error)
                
            if self.check_duplicado_referencia(referencia_id):
                raise ValidationError("Error: Este cliente ya tiene esta referencia creada")
                
            self.referencia_id = referencia_id    
            self.state = 'REF'
            self.referencia_cliente_nombre = self.referencia_id.titulo
            
            
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
                
            if self.check_duplicado_referencia(referencia_id):
                raise ValidationError("Error: Este cliente ya tiene esta referencia creada")
                
            self.referencia_id = referencia_id    
            self.state = 'REF'
            self.referencia_cliente_nombre = self.referencia_id.titulo
            
            
        
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

    referencia_cliente_id = fields.Many2one('sale.referencia.cliente', string="Referencia cliente", ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Cliente', store=True, related='referencia_cliente_id.partner_id')
    type_id = fields.Many2one('product.category', string="Tipo de producto", store=True, related='referencia_cliente_id.type_id')
    is_cantonera = fields.Boolean('¿Es Cantonera?', related='type_id.is_cantonera')
    is_perfilu = fields.Boolean('¿Es Perfil U?', related='type_id.is_perfilu')
    is_slipsheet = fields.Boolean('¿Es Slip Sheet?', related='type_id.is_slipsheet')
    is_solidboard = fields.Boolean('¿Es Solid Board?', related='type_id.is_solidboard')
    is_formato = fields.Boolean('¿Es Formato?', related='type_id.is_formato')
    is_bobina = fields.Boolean('¿Es Bobina?', related='type_id.is_bobina')
    is_pieballet = fields.Boolean('¿Es Pie de Ballet?', related='type_id.is_pieballet')
    is_flatboard = fields.Boolean('¿Es Flat Board?', related='type_id.is_flatboard')
    is_varios = fields.Boolean('¿Es Varios?', related='type_id.is_varios')
    
    activa = fields.Boolean("Activa", default = True)
    
    name = fields.Char('Nombre Interno', readonly = True, compute = "_get_titulo")
    estado = fields.Char('Estado', readonly = True, compute = "_get_titulo")
    titulo = fields.Html('Descripción para el Cliente', readonly = True, compute = "_get_titulo")
    producto_texto = fields.Char('Producto Texto', readonly = True, compute = "_get_titulo")
    atributo_texto = fields.Char('Producto Texto', readonly = True, compute = "_get_titulo")
    comentario_proveedor = fields.Char('Comentario Proveedor')
    descripcion_proveedor = fields.Html('Descripcion Proveedor', readonly = True, compute = "_get_titulo")
    
    #CANTONERA COLOR
    cantonera_color_id = fields.Many2one('product.caracteristica.cantonera.color', string="Cantonera Color")
    cantonera_forma_id = fields.Many2one('product.caracteristica.cantonera.forma', string="Forma")
    cantonera_especial_id = fields.Many2one('product.caracteristica.cantonera.especial', string="Especial")
    cantonera_impresion_id = fields.Many2one('product.caracteristica.cantonera.impresion', string="Impresión")
    cantonera_cliche_id = fields.Many2one('product.caracteristica.cliche', string="Cliché")
    
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
    
    no_editar = fields.Boolean('No Editar')
    referencia_cliente_nombre = fields.Char('Referencia_cliente_nombre', readonly = True)
    paletizado = fields.Integer('Paletizado', readonly = True)
    ancho_pallet = fields.Integer('Ancho Pallet', readonly = True)
    pallet_especial_id = fields.Many2one('product.caracteristica.pallet.especial', readonly = True, string = "Pallet especial")
    und_paquete = fields.Integer('Und Paquete', readonly = True)
    paquetes_fila = fields.Integer('Paquetes Fila', readonly = True)
    

    @api.onchange('referencia_cliente_id')
    def _onchange_referencia_cliente(self):
        self.referencia_cliente_nombre = self.referencia_cliente_id.referencia_cliente_nombre
        self.paletizado = self.referencia_cliente_id.paletizado
        self.ancho_pallet = self.referencia_cliente_id.ancho_pallet
        self.pallet_especial_id = self.referencia_cliente_id.pallet_especial_id
        self.und_paquete = self.referencia_cliente_id.und_paquete
        self.paquetes_fila = self.referencia_cliente_id.paquetes_fila
    
    
    #OFERTA
    oferta_ids = fields.One2many('sale.offer.oferta', 'attribute_id', string="Ofertas", copy=True)
    
    
    @api.depends('type_id', 'cantonera_color_id', 'cantonera_forma_id', 'cantonera_especial_id', 'inglete_num', 'inglete_id', 'perfilu_color_id', 'troquelado_id', 'papel_calidad_id', 'fsc_id', 'reciclable_id')
    def _get_titulo(self):
        for record in self:
            nombre = ''
            estado = ''
            descripcion = ''
            titulo = ''
            proveedor = ''
            
            producto_texto = ""
            atributo_texto = ""

            if record.referencia_cliente_id:
                
                #Varios
                if record.type_id.is_varios == True:
                    nombre = record.referencia_cliente_id.referencia_id.tipo_varios_id.name + ", "
                    if record.referencia_cliente_id.referencia_id.tipo_varios_id.description:
                        titulo = record.referencia_cliente_id.referencia_id.tipo_varios_id.description
                    else:
                        titulo = "Varios"
                    
                #Cantonera
                elif record.type_id.is_cantonera == True:
                    titulo = "Cantonera "
                    if record.cantonera_color_id:
                        nombre = nombre + record.cantonera_color_id.name + ", "
                        if record.cantonera_color_id.description and record.cantonera_color_id.valido == True:
                            titulo = titulo + record.cantonera_color_id.description
                        else:
                            estado = estado + "Falta Color, "
                    else:
                        nombre = nombre + "Sin Color, "
                        estado = estado + "Falta Color, "
                    if record.fsc_id:
                        nombre = nombre + record.fsc_id.name + ", "
                        if record.fsc_id.description:
                            titulo = titulo + record.fsc_id.description
                    
                    if record.referencia_cliente_nombre:
                        if record.referencia_cliente_nombre != "":
                            titulo = titulo + "<br/>" + record.referencia_cliente_nombre
                        
                    if record.cantonera_especial_id:
                        nombre = nombre + record.cantonera_especial_id.name + ", "
                        if record.cantonera_especial_id.description:
                            descripcion = descripcion + record.cantonera_especial_id.description + ", "
                            
                    if record.cantonera_impresion_id:
                        nombre = nombre + record.cantonera_impresion_id.name
                        if record.cantonera_impresion_id.description:
                            descripcion = descripcion + record.cantonera_impresion_id.description
                        if record.cantonera_cliche_id:
                            if record.cantonera_cliche_id.description:
                                nombre = nombre + " (" + record.cantonera_cliche_id.description + "), "
                                descripcion = descripcion + " (" + record.cantonera_cliche_id.description + "), "
                        else:
                            nombre = nombre + ", "
                            descripcion = descripcion + ", "
                    if record.inglete_num > 0 and record.inglete_id:
                        nombre = nombre + str(record.inglete_num) + " " + record.inglete_id.name + ", "
                        if record.inglete_id.description:
                            descripcion = descripcion + str(record.inglete_num) + " " + record.inglete_id.description + ", "
                    if record.cantonera_forma_id:
                        nombre = nombre + record.cantonera_forma_id.name + ", "
                        if record.cantonera_forma_id.description:
                            descripcion = descripcion + record.cantonera_forma_id.description + ", "
                    else:
                        nombre = nombre + "Canto Recto, "
                    if record.reciclable_id:
                        nombre = nombre + record.reciclable_id.name + ", "
                        if record.reciclable_id.description:
                            descripcion = descripcion + record.reciclable_id.description + ", "
                    
                    if descripcion != "":
                        titulo = titulo + "<br/>" + descripcion[:-2]
                    
                #Perfil U
                elif record.type_id.is_perfilu == True:
                    titulo = "Perfil U "
                    if record.perfilu_color_id:
                        nombre = nombre + record.perfilu_color_id.name + ", "
                        if record.perfilu_color_id.description:
                            titulo = titulo + record.perfilu_color_id.description
                    else:
                        nombre = nombre + "Sin Color, "
                        estado = estado + "Falta Color, "
                    if record.fsc_id:
                        nombre = nombre + record.fsc_id.name + ", "
                        if record.fsc_id.description:
                            titulo = titulo + record.fsc_id.description
                    
                    if record.referencia_cliente_nombre:
                        if record.referencia_cliente_nombre != "":
                            titulo = titulo + "<br/>" + record.referencia_cliente_nombre
                    
                    if record.inglete_num > 0 and record.inglete_id:
                        nombre = nombre + str(record.inglete_num) + " " + record.inglete_id.name + ", "
                        if record.inglete_id.description:
                            descripcion = descripcion + str(record.inglete_num) + " " + record.inglete_id.description + ", "
                            
                    if descripcion != "":
                        titulo = titulo + "<br/>" + descripcion[:-2]
                    
                #Slip Sheets
                elif record.type_id.is_slipsheet == True:
                    titulo = "Slip Sheet "
                    
                    if record.fsc_id:
                        nombre = nombre + record.fsc_id.name + ", "
                        if record.fsc_id.description:
                            titulo = titulo + record.fsc_id.description
                    
                    if record.referencia_cliente_nombre:
                        if record.referencia_cliente_nombre != "":
                            titulo = titulo + "<br/>" + record.referencia_cliente_nombre

                    if record.troquelado_id:
                        nombre = nombre + record.troquelado_id.name + ", "
                        if record.troquelado_id.description:
                            descripcion = descripcion + record.troquelado_id.description + ", "
                    else:
                        nombre = nombre + "Falta Troquelado, "
                        estado = estado + "Falta Troquelado, "
                    
                    if descripcion != "":
                        titulo = titulo + "<br/>" + descripcion[:-2]
                    
                #Solid Board
                elif record.type_id.is_solidboard == True:
                    titulo = "Solid Board "
                    if record.plancha_color_id:
                        nombre = nombre + record.plancha_color_id.name + ", "
                        if record.plancha_color_id.description:
                            titulo = titulo + record.plancha_color_id.description
                    else:
                        nombre = nombre + "Sin Color, "
                        estado = estado + "Falta Color, "
                    
                    if record.fsc_id:
                        nombre = nombre + record.fsc_id.name + ", "
                        if record.fsc_id.description:
                            titulo = titulo + record.fsc_id.description
                    
                    if record.referencia_cliente_nombre:
                        if record.referencia_cliente_nombre != "":
                            titulo = titulo + "<br/>" + record.referencia_cliente_nombre
                        
                    if record.troquelado_id:
                        nombre = nombre + record.troquelado_id.name + ", "
                        if record.troquelado_id.description:
                            descripcion = descripcion + record.troquelado_id.description + ", "
                            
                    if descripcion != "":
                        titulo = titulo + "<br/>" + descripcion[:-2]
                    
                #Formato
                elif record.type_id.is_formato == True:
                    titulo = "Formato "
                    if record.papel_calidad_id:
                        nombre = nombre + record.papel_calidad_id.name + ", "
                        if record.papel_calidad_id.description:
                            titulo = titulo + record.papel_calidad_id.description
                    else:
                        nombre = nombre + "Falta Papel, "
                        estado = estado + "Falta Papel, "
                    if record.fsc_id:
                        nombre = nombre + record.fsc_id.name + ", "
                        if record.fsc_id.description:
                            titulo = titulo + record.fsc_id.description + "</br>"
                    
                    if record.referencia_cliente_nombre:
                        if record.referencia_cliente_nombre != "":
                            titulo = titulo + "<br/>" + record.referencia_cliente_nombre
                    
                    if record.troquelado_id:
                        nombre = nombre + record.troquelado_id.name + ", "
                        if record.troquelado_id.descripcion:
                            descripcion = descripcion + record.troquelado_id.description + ", "
                    
                    if descripcion != "":
                        titulo = titulo + "<br/>" + descripcion[:-2]
                    
                #Bobina
                elif record.type_id.is_bobina == True:
                    titulo = "Bobina "
                    if record.papel_calidad_id:
                        nombre = nombre + record.papel_calidad_id.name + ", "
                        if record.papel_calidad_id.description:
                            titulo = titulo + record.papel_calidad_id.description
                    else:
                        nombre = nombre + "Falta Papel, "
                        estado = estado + "Falta Papel, "                
                    if record.fsc_id:
                        nombre = nombre + record.fsc_id.name + ", "
                        if record.fsc_id.description:
                            titulo = titulo + record.fsc_id.description
                    
                    if record.referencia_cliente_nombre:
                        if record.referencia_cliente_nombre != "":
                            titulo = titulo + "<br/>" + record.referencia_cliente_nombre
                    
                #Pie de Pallet
                elif record.type_id.is_pieballet == True:
                    titulo = "Pie de Pallet "
                    nombre = nombre  + "Pie de Pallet, "
                    if record.referencia_cliente_nombre:
                        if record.referencia_cliente_nombre != "":
                            titulo = titulo + "<br/>" + record.referencia_cliente_nombre
                    
                #Flat Board
                elif record.type_id.is_flatboard == True:
                    titulo = "Flat Board "
                    if record.perfilu_color_id:
                        nombre = nombre + record.perfilu_color_id.name + ", "
                        if record.perfilu_color_id.description:
                            titulo = titulo + record.perfilu_color_id.description
                    else:
                        nombre = nombre + "Sin Color, "
                        estado = estado + "Falta Color, "
                    if record.fsc_id:
                        nombre = nombre + record.fsc_id.name + ", "
                        if record.fsc_id.description:
                            titulo = titulo + record.fsc_id.description
                    
                    if record.referencia_cliente_nombre:
                        if record.referencia_cliente_nombre != "":
                            titulo = titulo + "<br/>" + record.referencia_cliente_nombre
                    
            
            if len(nombre) > 2:
                nombre = nombre[:-2]
            if len(estado) > 2:
                estado = estado[:-2]

            proveedor = titulo
            
            if nombre == '':
                nombre = 'Nuevo'
            record.name = nombre
            record.titulo = titulo
            record.descripcion_proveedor = proveedor
            record.estado = estado
            record.producto_texto = producto_texto
            record.atributo_texto = atributo_texto
    


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
    def _get_valores(self):
        for record in self:
            sierra = False

            if record.referencia_cliente_id:

                #Cantonera
                if record.type_id.is_cantonera == True:
                    if record.referencia_cliente_id.longitud < 500:
                        sierra = True

                    
                #Perfil U
                elif record.type_id.is_perfilu == True:
                    if record.referencia_cliente_id.longitud < 400:
                        sierra = True

            record.sierra = sierra
            
    
    
    
    
    
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
    

    
    
class sale_offer_oferta(models.Model):
    _name = 'sale.offer.oferta'
    
    partner_id = fields.Many2one('res.partner', string='Cliente', store=True, related='attribute_id.referencia_cliente_id.partner_id')
    referencia_cliente_id = fields.Many2one('sale.referencia.cliente', string='Referencia cliente', ondelete='cascade')
    attribute_id = fields.Many2one('sale.product.attribute', string="Atributo producto", required=True, ondelete='cascade' )
    
    PRECIO_SEL = [('1', 'metro / metro2'),     
                  ('2', 'unidad'),
                  ('3', 'millar'),
                  ('4', 'kilos'), 
                  ('5', 'varios unidad'), 
                  ]
    precio_cliente = fields.Selection(selection = PRECIO_SEL, string = 'Facturar por:', related='referencia_cliente_id.precio_cliente', store=True)
    
    #IZQUIERDA
    user_id = fields.Many2one('res.users', string="Comercial", default=lambda self: self.env.user, required=True)
    date = fields.Date('Fecha', default=fields.Date.today(), required=True)
    activa = fields.Boolean("Activa", default = True)
    state_id = fields.Many2one('res.country.state', string="Provincia")
    country_id = fields.Many2one('res.country', string="País")
    num_pallets = fields.Integer('Número Pallets', default = 1)
    und_exactas = fields.Boolean('Unidades Exactas')
    no_editar = fields.Boolean('No editar')
    
    unidades = fields.Integer('Unidades Pallet', default = 1)
    precio_metro = fields.Float('Precio Metro', digits = (12,4))
    kilos = fields.Integer('Kilos Pallet')
    precio_kilo = fields.Float('Precio kilo', digits = (12,4))
    precio_varios = fields.Float('Precio Varios Unidad', digits = (12,4))
    cliente_final = fields.Char('Cliente Final')
    
    #DERECHA
    peso_metro = fields.Float('Peso Metro', digits = (12,4), readonly = True, related='referencia_cliente_id.referencia_id.peso_metro')
    
    tarifa_id = fields.Many2one('product.pricelist.oferta', string="Tarifa")
    alto_pallet = fields.Integer('Alto', readonly = True, compute = "_get_alto_pallet")
    peso_neto = fields.Integer('Peso Neto', readonly = True, compute = "_get_peso_neto")
    peso_bruto = fields.Integer('Peso Bruto', readonly = True, compute = "_get_peso_bruto")
    und_pallet = fields.Integer('Propuesta Unidades', readonly = True, compute = "_get_und_pallet")
    
    alto_pallet_text = fields.Char('Alto', readonly = True, compute = "_get_alto_pallet_text")
    peso_neto_text = fields.Char('Peso Neto', readonly = True, compute = "_get_peso_neto_text")
    peso_bruto_text = fields.Char('Peso Bruto', readonly = True, compute = "_get_peso_bruto_text")
    und_pallet_text = fields.Char('Propuesta Unidades', readonly = True, compute = "_get_und_pallet_text")
    
    in_corte = fields.Boolean('Incluir Corte en precio metro', default = True)
    eton_user = fields.Float('Euros / Tonelada', digits = (8,1))
    emetro_calculado = fields.Float('Calculo € / m', digits = (12,4), readonly = True, compute = "_get_calculado")
    eton_calculado = fields.Float('Calculo € / ton', digits = (8,1), readonly = True, compute = "_get_calculado")
    
    #OCULTOS
    num_filas = fields.Integer('Num filas', readonly = True)
    fecha_enviada = fields.Date('Fecha Enviada')
    
    name = fields.Char('Título', readonly = True, compute = "_get_precio")
    cantidad = fields.Float('Cantidad', digits = (12,4), readonly = True, compute = "_get_precio")
    cantidad_tipo = fields.Char('Cantidad Tipo', readonly = True, compute = "_get_precio")
    precio = fields.Float('Precio', digits = (12,4), readonly = True, compute = "_get_precio")
    precio_tipo = fields.Char('Precio Tipo', readonly = True, compute = "_get_precio")
    
    estado = fields.Char('Estado', compute = "_get_estado")
    
    @api.multi
    def suma_filas(self):
        for record in self:
            if record.attribute_id.referencia_cliente_id.und_pallet_cliente > 0:
                raise ValidationError("Unidades Exactas")
            elif record.attribute_id.referencia_cliente_id.fila_buena + record.num_filas < self.attribute_id.referencia_cliente_id.fila_max:
                record.num_filas = record.num_filas + 1
            
    @api.multi
    def resta_filas(self):
        for record in self:
            if record.attribute_id.referencia_cliente_id.und_pallet_cliente > 0:
                raise ValidationError("Unidades Exactas")
            elif record.attribute_id.referencia_cliente_id.fila_buena + record.num_filas > 0:
                record.num_filas = record.num_filas - 1
    

    @api.depends('attribute_id', 'num_filas',)
    def _get_und_pallet(self):
        for record in self:
            und = 0
            if record.attribute_id.referencia_cliente_id.und_pallet_cliente > 0:
                und = record.attribute_id.referencia_cliente_id.und_pallet_cliente
            else:
                undFila = record.attribute_id.referencia_cliente_id.und_paquete * record.attribute_id.referencia_cliente_id.paquetes_fila
                und = undFila * (record.num_filas + record.attribute_id.referencia_cliente_id.fila_buena)
                
            record.und_pallet = und
    
    
    @api.depends('und_pallet')
    def _get_und_pallet_text(self):
        for record in self:
            texto = str(record.und_pallet) + " unidades/pallet"
            record.und_pallet_text = texto
    
    
    
    @api.depends('attribute_id', 'und_pallet')
    def _get_peso_neto(self):
        for record in self:
            und = record.und_pallet
            pesoUnd = record.attribute_id.referencia_cliente_id.referencia_id.peso_metro * record.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
            peso = und * pesoUnd
            record.peso_neto = peso
    
    
    @api.depends('peso_neto')
    def _get_peso_neto_text(self):
        for record in self:
            texto = str(record.peso_neto) + " kg/pallet"
            record.peso_neto_text = texto
    
    
    @api.depends('attribute_id', 'peso_neto')
    def _get_peso_bruto(self):
        for record in self:
            peso = record.peso_neto
            pesoMadera = 0
            if record.attribute_id.referencia_cliente_id.referencia_id.longitud < 1500:
                pesoMadera = 20
            elif record.attribute_id.referencia_cliente_id.referencia_id.longitud < 2000:
                pesoMadera = 30
            else:
                pesoMadera = int(self.attribute_id.referencia_cliente_id.referencia_id.longitud / 1000) * 20
            peso = int((peso + pesoMadera) / 5) * 5
            record.peso_bruto = peso
    
    
    @api.depends('peso_neto')
    def _get_peso_bruto_text(self):
        for record in self:
            texto = str(record.peso_bruto) + " kg/pallet"
            record.peso_bruto_text = texto
            
        
    @api.depends('attribute_id', 'num_filas')
    def _get_alto_pallet(self):
        for record in self:
            alto = record.attribute_id.referencia_cliente_id.alto_fila * (record.num_filas + record.attribute_id.referencia_cliente_id.fila_buena) + 150
            alto = int(alto / 5) * 5
            record.alto_pallet = alto
     
    
    @api.depends('alto_pallet')
    def _get_alto_pallet_text(self):
        for record in self:
            texto = str(record.alto_pallet) + " mm"
            record.alto_pallet_text = texto
           
        
    @api.depends('eton_user', 'und_pallet', 'tarifa_id')
    def _get_calculado(self):
        for record in self:
            emetro = 0
            eton = 0
            in_metro = 0
            in_unidad = 0
            in_porcentaje = 0
            in_pallet = 0
            
            in_pallet_especial = True
            in_fsc = True
            in_reciclable = True
            in_cantonera_color = True
            in_cantonera_forma = True
            in_cantonera_especial = True
            in_cantonera_impresion = True
            in_perfilu_color = True
            in_inglete = True
            in_plancha_color = True
            in_papel_calidad = True
            in_troquelado = True
            
            if record.tarifa_id:
                if record.tarifa_id.eton > 0:
                    eton = record.tarifa_id.eton
                in_pallet_especial = record.tarifa_id.inpallet_especial
                in_fsc = record.tarifa_id.in_fsc
                in_reciclable = record.tarifa_id.in_reciclable
                in_cantonera_color = record.tarifa_id.in_cantonera_color
                in_cantonera_forma = record.tarifa_id.in_cantonera_forma
                in_cantonera_especial = record.tarifa_id.in_cantonera_especial
                in_cantonera_impresion = record.tarifa_id.in_cantonera_impresion
                in_perfilu_color = record.tarifa_id.in_perfilu_color
                in_inglete = record.tarifa_id.in_inglete
                in_plancha_color = record.tarifa_id.in_plancha_color
                in_papel_calidad = record.tarifa_id.in_papel_calidad
                in_troquelado = record.tarifa_id.in_troquelado
                
            elif record.eton_user > 0:
                eton = record.eton_user

            if in_pallet_especial == True and record.attribute_id.referencia_cliente_id.pallet_especial_id:
                if record.attribute_id.referencia_cliente_id.pallet_especial_id.incremento > 0 and record.attribute_id.referencia_cliente_id.pallet_especial_id.tipo:
                    if record.attribute_id.referencia_cliente_id.pallet_especial_id.tipo == '1':
                        in_metro = in_metro + record.attribute_id.referencia_cliente_id.pallet_especial_id.incremento
                    elif record.attribute_id.referencia_cliente_id.pallet_especial_id.tipo == '2':
                        in_unidad = in_unidad + record.attribute_id.referencia_cliente_id.pallet_especial_id.incremento
                    elif record.attribute_id.referencia_cliente_id.pallet_especial_id.tipo == '3':
                        in_porcentaje = in_porcentaje + record.attribute_id.referencia_cliente_id.pallet_especial_id.incremento
                    elif record.attribute_id.referencia_cliente_id.pallet_especial_id.tipo == '4':
                        in_pallet = in_pallet + record.attribute_id.referencia_cliente_id.pallet_especial_id.incremento
            
            
            if in_fsc == True and record.attribute_id.fsc_id:
                if record.attribute_id.fsc_id.incremento > 0 and record.attribute_id.fsc_id.tipo:
                    if record.attribute_id.fsc_id.tipo == '1':
                        in_metro = in_metro + record.attribute_id.fsc_id.incremento
                    elif record.attribute_id.fsc_id.tipo == '2':
                        in_unidad = in_unidad + record.attribute_id.fsc_id.incremento
                    elif record.attribute_id.fsc_id.tipo == '3':
                        in_porcentaje = in_porcentaje + record.attribute_id.fsc_id.incremento
                    elif record.attribute_id.fsc_id.tipo == '4':
                        in_pallet = in_pallet + record.attribute_id.fsc_id.incremento
            """
            if in_reciclable == True and record.attribute_id.reciclable_id:
                if record.attribute_id.reciclable_id.incremento > 0 and record.attribute_id.reciclable_id.tipo:
                    if record.attribute_id.reciclable_id.tipo == '1':
                        in_metro = in_metro + record.attribute_id.reciclable_id.incremento
                    elif record.attribute_id.reciclable_id.tipo == '2':
                        in_unidad = in_unidad + record.attribute_id.reciclable_id.incremento
                    elif record.attribute_id.reciclable_id.tipo == '3':
                        in_porcentaje = in_porcentaje + record.attribute_id.reciclable_id.incremento
                    elif record.attribute_id.reciclable_id.tipo == '4':
                        in_pallet = in_pallet + record.attribute_id.reciclable_id.incremento
                        
            if in_cantonera_color == True and record.attribute_id.cantonera_color_id:
                if record.attribute_id.cantonera_color_id.incremento > 0 and record.attribute_id.cantonera_color_id.tipo:
                    if record.attribute_id.cantonera_color_id.tipo == '1':
                        in_metro = in_metro + record.attribute_id.cantonera_color_id.incremento
                    elif record.attribute_id.cantonera_color_id.tipo == '2':
                        in_unidad = in_unidad + record.attribute_id.cantonera_color_id.incremento
                    elif record.attribute_id.cantonera_color_id.tipo == '3':
                        in_porcentaje = in_porcentaje + record.attribute_id.cantonera_color_id.incremento
                    elif record.attribute_id.cantonera_color_id.tipo == '4':
                        in_pallet = in_pallet + record.attribute_id.cantonera_color_id.incremento
            
            if in_cantonera_forma == True and record.attribute_id.cantonera_forma_id:
                if record.attribute_id.cantonera_forma_id.incremento > 0 and record.attribute_id.cantonera_forma_id.tipo:
                    if record.attribute_id.cantonera_forma_id.tipo == '1':
                        in_metro = in_metro + record.attribute_id.cantonera_forma_id.incremento
                    elif record.attribute_id.cantonera_forma_id.tipo == '2':
                        in_unidad = in_unidad + record.attribute_id.cantonera_forma_id.incremento
                    elif record.attribute_id.cantonera_forma_id.tipo == '3':
                        in_porcentaje = in_porcentaje + record.attribute_id.cantonera_forma_id.incremento
                    elif record.attribute_id.cantonera_forma_id.tipo == '4':
                        in_pallet = in_pallet + record.attribute_id.cantonera_forma_id.incremento

            if in_cantonera_especial == True and record.attribute_id.cantonera_especial_id:
                if record.attribute_id.cantonera_especial_id.incremento > 0 and record.attribute_id.cantonera_especial_id.tipo:
                    if record.attribute_id.cantonera_especial_id.tipo == '1':
                        in_metro = in_metro + record.attribute_id.cantonera_especial_id.incremento
                    elif record.attribute_id.cantonera_especial_id.tipo == '2':
                        in_unidad = in_unidad + record.attribute_id.cantonera_especial_id.incremento
                    elif record.attribute_id.cantonera_especial_id.tipo == '3':
                        in_porcentaje = in_porcentaje + record.attribute_id.cantonera_especial_id.incremento
                    elif record.attribute_id.cantonera_especial_id.tipo == '4':
          
            if in_cantonera_impresion == True and record.attribute_id.cantonera_impresion_id:
                if record.attribute_id.cantonera_impresion_id.incremento > 0 and record.attribute_id.cantonera_impresion_id.tipo:
                    if record.attribute_id.cantonera_impresion_id.tipo == '1':
                        in_metro = in_metro + record.attribute_id.cantonera_impresion_id.incremento
                    elif record.attribute_id.cantonera_impresion_id.tipo == '2':
                        in_unidad = in_unidad + record.attribute_id.cantonera_impresion_id.incremento
                    elif record.attribute_id.cantonera_impresion_id.tipo == '3':
                        in_porcentaje = in_porcentaje + record.attribute_id.cantonera_impresion_id.incremento
                    elif record.attribute_id.cantonera_impresion_id.tipo == '4':
                        in_pallet = in_pallet + record.attribute_id.cantonera_impresion_id.incremento

            if in_perfilu_color == True and record.attribute_id.perfilu_color_id:
                if record.attribute_id.perfilu_color_id.incremento > 0 and record.attribute_id.perfilu_color_id.tipo:
                    if record.attribute_id.perfilu_color_id.tipo == '1':
                        in_metro = in_metro + record.attribute_id.perfilu_color_id.incremento
                    elif record.attribute_id.perfilu_color_id.tipo == '2':
                        in_unidad = in_unidad + record.attribute_id.perfilu_color_id.incremento
                    elif record.attribute_id.perfilu_color_id.tipo == '3':
                        in_porcentaje = in_porcentaje + record.attribute_id.perfilu_color_id.incremento
                    elif record.attribute_id.perfilu_color_id.tipo == '4':
                        in_pallet = in_pallet + record.attribute_id.perfilu_color_id.incremento
            
            if in_inglete == True and record.attribute_id.inglete_id:
                if record.attribute_id.inglete_id.incremento > 0 and record.attribute_id.inglete_id.tipo:
                    if record.attribute_id.inglete_id.tipo == '1':
                        in_metro = in_metro + record.attribute_id.inglete_id.incremento
                    elif record.attribute_id.inglete_id.tipo == '2':
                        in_unidad = in_unidad + record.attribute_id.inglete_id.incremento
                    elif record.attribute_id.inglete_id.tipo == '3':
                        in_porcentaje = in_porcentaje + record.attribute_id.inglete_id.incremento
                    elif record.attribute_id.inglete_id.tipo == '4':
                        in_pallet = in_pallet + record.attribute_id.inglete_id.incremento
            
            if in_plancha_color == True and record.attribute_id.plancha_color_id:
                if record.attribute_id.plancha_color_id.incremento > 0 and record.attribute_id.plancha_color_id.tipo:
                    if record.attribute_id.plancha_color_id.tipo == '1':
                        in_metro = in_metro + record.attribute_id.plancha_color_id.incremento
                    elif record.attribute_id.plancha_color_id.tipo == '2':
                        in_unidad = in_unidad + record.attribute_id.plancha_color_id.incremento
                    elif record.attribute_id.plancha_color_id.tipo == '3':
                        in_porcentaje = in_porcentaje + record.attribute_id.plancha_color_id.incremento
                    elif record.attribute_id.plancha_color_id.tipo == '4':
                        in_pallet = in_pallet + record.attribute_id.plancha_color_id.incremento
            
            if in_papel_calidad == True and record.attribute_id.papel_calidad_id:
                if record.attribute_id.papel_calidad_id.incremento > 0 and record.attribute_id.papel_calidad_id.tipo:
                    if record.attribute_id.papel_calidad_id.tipo == '1':
                        in_metro = in_metro + record.attribute_id.papel_calidad_id.incremento
                    elif record.attribute_id.papel_calidad_id.tipo == '2':
                        in_unidad = in_unidad + record.attribute_id.papel_calidad_id.incremento
                    elif record.attribute_id.papel_calidad_id.tipo == '3':
                        in_porcentaje = in_porcentaje + record.attribute_id.papel_calidad_id.incremento
                    elif record.attribute_id.papel_calidad_id.tipo == '4':
                        in_pallet = in_pallet + record.attribute_id.papel_calidad_id.incremento

            if in_troquelado == True and record.attribute_id.troquelado_id:
                if record.attribute_id.troquelado_id.incremento > 0 and record.attribute_id.troquelado_id.tipo:
                    if record.attribute_id.troquelado_id.tipo == '1':
                        in_metro = in_metro + record.attribute_id.troquelado_id.incremento
                    elif record.attribute_id.troquelado_id.tipo == '2':
                        in_unidad = in_unidad + record.attribute_id.troquelado_id.incremento
                    elif record.attribute_id.troquelado_id.tipo == '3':
                        in_porcentaje = in_porcentaje + record.attribute_id.troquelado_id.incremento
                    elif record.attribute_id.troquelado_id.tipo == '4':
                        in_pallet = in_pallet + record.attribute_id.troquelado_id.incremento        

            """
            if eton > 0:
                emetro = eton * record.attribute_id.referencia_cliente_id.referencia_id.peso_metro / 1000
                #Incremento por porcentaje
                emetro = emetro * (1 + in_porcentaje / 100)
                #Incremento por metro
                emetro = emetro + in_metro
                #Por unidad
                eunidad = emetro * record.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
                #Incremento por unidad
                eunidad = eunidad + in_unidad
                #Incremento por pallet
                if record.und_pallet > 0:
                    eunidad = eunidad + in_pallet / record.und_pallet
                #Incremento de corte
                if record.in_corte and record.attribute_id.sierra:
                    eunidad = eunidad + 0.017
                #Calculo precio metro
                if record.attribute_id.referencia_cliente_id.referencia_id.metros_unidad > 0:
                    emetro = eunidad / record.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
                emetro = int(emetro * 1000) / 1000
                #Calculo precio ton
                if record.attribute_id.referencia_cliente_id.referencia_id.peso_metro > 0:
                    eton = emetro * 10000 / record.attribute_id.referencia_cliente_id.referencia_id.peso_metro
                eton = int(eton + 1) / 10
            
            record.emetro_calculado = emetro
            record.eton_calculado = eton
            
            
            
    @api.depends('attribute_id', 'unidades', 'alto_pallet')
    def _get_estado(self):
        for record in self:
            estado = ""
            if record.attribute_id.referencia_cliente_id.und_pallet_cliente > 0 and record.unidades != record.attribute_id.referencia_cliente_id.und_pallet_cliente:
                estado = "Unidades Incorrectas"
            elif record.alto_pallet > 1250:
                estado = "No remontable"
            elif record.alto_pallet > 1100 and record.attribute_id.referencia_cliente_id.contenedor == True:
                estado = "No remontable"
                
            record.estado = estado

            
    
    @api.depends('attribute_id', 'num_pallets', 'unidades', 'precio_metro', 'kilos', 'precio_kilo')
    def _get_precio(self):
        for record in self:
            facturar = record.attribute_id.referencia_cliente_id.precio_cliente
            cantidad = 0
            cantidad_texto = ""
            cantidad_tipo = ""
            precio = 0
            precio_tipo = ""
            nombre = ""
            #Por metro
            if facturar == '1':
                cantidad = record.unidades * record.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
                cantidad_tipo = "metros"
                aux = cantidad * 10000
                decimales = 4
                while aux % 10 == 0 and decimales > 1:
                    aux = aux / 10
                    decimales = decimales - 1
                
                aux = aux / (decimales * 10)
                cantidad_texto = str(aux)
                precio = record.precio_metro
                precio = round(precio, 4)
                precio_tipo = "€/metro"
                eton = record.precio_metro * 1000 / record.attribute_id.referencia_cliente_id.referencia_id.peso_metro
                eton = round(eton, 1)
                nombre = str(record.num_pallets) + " pallets, " + str(record.unidades) + " und/pallet, "
                nombre = nombre + str(precio) + " €/m, " + str(eton) + " €/t"
            #Por unidad
            elif facturar == '2':
                cantidad = record.unidades
                cantidad_tipo = "unidades"
                precio = record.precio_metro * record.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
                precio = round(precio, 4)
                precio_tipo = "€/unidad" 
                eton = record.precio_metro * 1000 / record.attribute_id.referencia_cliente_id.referencia_id.peso_metro
                eton = round(eton, 1)
                nombre = str(record.num_pallets) + " pallets, " + str(record.unidades) + " und/pallet, "
                nombre = nombre + str(precio) + " €/unidad, " + str(eton) + " €/t"
            #Por millar
            elif facturar == '3':
                cantidad = record.unidades / 1000
                cantidad_tipo = "millares"
                precio = record.precio_metro * record.attribute_id.referencia_cliente_id.referencia_id.metros_unidad * 1000
                precio = round(precio, 4)
                precio_tipo = "€/millar" 
                eton = record.precio_metro * 1000 / record.attribute_id.referencia_cliente_id.referencia_id.peso_metro
                eton = round(eton, 1)
                nombre = str(record.num_pallets) + " pallets, " + str(record.unidades) + " und/pallet, "
                nombre = nombre + str(precio) + " €/millar, " + str(eton) + " €/t"
            elif facturar == '4':
                cantidad = record.kilos
                cantidad_tipo = "kg"
                precio = record.precio_kilo
                precio = round(precio, 4)
                precio_tipo = "€/kg" 
                eton = precio * 1000
                nombre = str(record.num_pallets) + " pallets, " + str(record.kilos) + " kg/pallet, "
                nombre = nombre + str(precio) + " €/kg, " + str(eton) + " €/t"
            elif facturar == '5':
                cantidad = 1
                cantidad_tipo = "unidades"
                precio = record.precio_varios
                precio = round(precio, 4)
                precio_tipo = "€/unidad" 
                eton = 0
                nombre = str(precio) + " €/unidad"

            record.name = nombre
            record.cantidad = cantidad
            record.cantidad_tipo = cantidad_tipo
            record.precio = precio
            record.precio_tipo = precio_tipo

