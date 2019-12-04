
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

    
class sale_referencia_cliente(models.Model):
    _name = 'sale.referencia.cliente'

    name = fields.Char(string='Ref cliente nombre', required=True, default=lambda self: "/")
    
    
    partner_id = fields.Many2one('res.partner', string="Cliente", required=True)
    user_id = fields.Many2one('res.users', string="Comercial", default=lambda self: self.env.user, required=True)
    date = fields.Date('Fecha', default=fields.Date.today(), required=True)
    
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
    
    
    ala_1 = fields.Integer('Ala 1')
    base = fields.Integer('Base')
    ala_2 = fields.Integer('Ala 2')
    grosor = fields.Float('Grosor')
    longitud = fields.Integer('Longitud')
    alas = fields.Integer('Alas')
    product_id = fields.Many2one('product.template', string="Producto", readonly=True)
    
    
    #REFERENCIA CLIENTE
    ancho_pallet_id = fields.Many2one('product.caracteristica.ancho', string="Ancho pallet")
    paletizado = fields.Integer('Paletizado')
    und_paquete = fields.Integer('Und Paquete') #
    paquetes_fila = fields.Integer('Paquetes Fila') #
    alturas = fields.Integer('Alturas')
    und_pallet = fields.Integer('Und pallet')
    und_paquete_cliente = fields.Integer('Und pallet cliente')
    alto_maximo_cliente = fields.Integer('Alto máximo cliente')
    und_pallet_cliente = fields.Integer('Und pallet cliente')
    comment = fields.Text("Comentario")
    
    attribute_ids = fields.One2many('sale.product.attribute', 'referencia_cliente_id', string="Atributos")
    #oferta_ids = fields.Many2many('sale.offer.oferta', string="Ofertas de la referencia", compute="_get_ofertas", readonly=True)
    oferta_ids = fields.One2many('sale.offer.oferta', 'referencia_cliente_id', string="Ofertas")
    
    
    
    
    
    

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
                
            product_id, error = self.type_id.create_prod_cantonera(self.ala_1, self.ala_2, self.grosor, self.longitud)
            
            if not product_id:
                raise ValidationError(error)
            self.product_id = product_id    
            self.state = 'REF'
            self.name = self.product_id.name
            
            
        if self.type_id.is_perfilu == True:
        
            if not self.ala_1 or self.ala_1 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ALA 1")
            if not self.base or self.base <= 0:
                raise ValidationError("Error: Hay que indicar un valor en BASE")
            if not self.ala_2 or self.ala_2 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ALA 2")
            if not self.grosor or self.grosor <= 0:
                raise ValidationError("Error: Hay que indicar un valor en GROSOR")
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
                
            product_id, error = self.type_id.create_prod_perfilu(self.ala_1, self.base, self.ala_2, self.grosor, self.longitud)
            
            if not product_id:
                raise ValidationError(error)
            self.product_id = product_id    
            self.state = 'REF'
            self.name = self.product_id.name
            
            
        
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
    oferta_ids = fields.One2many('sale.offer.oferta', 'attribute_id', string="Ofertas")
    
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
    
    
    
    
    
    
    
    
    
    