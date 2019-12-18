
from odoo import fields, models, api


class ProductReferencia(models.Model):
    _name = 'product.referencia'

    
    name = fields.Char('Nombre', readonly=True)
    
    #Se calcuculan cuando texto_error == ""
	####### - AÑADIR --> también al crear   -> titulo = fields.Char('Titulo', readonly = True, compute = getTitulo())
	
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
    ancho = fields.Integer('Ancho')
    ala_2 = fields.Integer('Ala 2')
    grosor = fields.Float('Grosor')
    grosor_1 = fields.Float('Grosor 1', digits=(6,1))
    grosor_2 = fields.Float('Grosor 2', digits=(8,2))
    longitud = fields.Integer('Longitud')
    alas = fields.Integer('Alas')
    interior = fields.Integer('Interior')
    entrada_1 = fields.Char('Entrada 1')
    entrada_2 = fields.Char('Entrada 2')
    entrada_3 = fields.Char('Entrada 3')
    entrada_4 = fields.Char('Entrada 4')
    
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
    
    comentario = fields.Text('Comentario Referencia')
    
    #varios
    peso_metro_user = fields.Float('Peso Metro', digits = (10,4))
    metros_unidad_user = fields.Float('Metros Unidad', digits = (10,4))
    
    
    #calculados
    peso_metro = fields.Float('Peso Metro', digits = (10,4), readonly = True, compute = "_get_peso_metro")
    metros_unidad = fields.Float('Metros Unidad', digits = (10,4), readonly = True, compute = "_get_valores_referencia")
    j_gram = fields.Integer('J Gram', readonly = True, compute = "_get_valores_referencia")
    j_interior = fields.Integer('J Interior', readonly = True, compute = "_get_valores_referencia")
    j_superficie = fields.Integer('J Superficie', readonly = True, compute = "_get_valores_referencia")
    
    
    @api.depends('type_id',)
    def _get_peso_metro(self):
    
        for record in self:
        
            peso1 = 0

            #Varios
            if record.type_id.is_varios == True and record.peso_metro_user > 0:
                peso1 = record.peso_metro_user
                
            #Cantonera
            elif record.type_id.is_cantonera == True:
                sumaAlas = record.ala_1 + record.ala_2
                if sumaAlas == 60:
                    peso1 = 385
                elif sumaAlas < 66:
                    peso1 = (425 - 385) / (66 - 60) * (sumaAlas - 60) + 385
                elif sumaAlas == 66:
                    peso1 = 425
                elif sumaAlas < 70:
                    peso1 = (450 - 425) / (70 - 66) * (sumaAlas - 66) + 425
                elif sumaAlas == 70:
                    peso1 = 450
                elif sumaAlas < 76:
                    peso1 = (510 - 450) / (76 - 70) * (sumaAlas - 70) + 450
                elif sumaAlas == 76:
                    peso1 = 510
                elif sumaAlas < 80:
                    peso1 = (535 - 510) / (80 - 76) * (sumaAlas - 76) + 510
                elif sumaAlas == 80:
                    peso1 = 535
                elif sumaAlas < 84:
                    peso1 = (560 - 535) / (84 - 80) * (sumaAlas - 80) + 535
                elif sumaAlas == 84:
                    peso1 = 560
                elif sumaAlas < 90:
                    peso1 = (600 - 560) / (90 - 84) * (sumaAlas - 84) + 560
                elif sumaAlas == 90:
                    peso1 = 600
                elif sumaAlas < 100:
                    peso1 = (700 - 600) / (100 - 90) * (sumaAlas - 90) + 600
                elif sumaAlas == 100:
                    peso1 = 700
                elif sumaAlas < 120:
                    peso1 = (835 - 700) / (120 - 100) * (sumaAlas - 100) + 700
                elif sumaAlas == 120:
                    peso1 = 835
                elif sumaAlas < 140:
                    peso1 = (875 - 835) / (140 - 120) * (sumaAlas - 120) + 835
                elif sumaAlas == 140:
                    peso1 = 875
                elif sumaAlas < 150:
                    peso1 = (940 - 875) / (150 - 140) * (sumaAlas - 140) + 875
                elif sumaAlas == 150:
                    peso1 = 940
                elif sumaAlas < 160:
                    peso1 = (1000 - 940) / (160 - 150) * (sumaAlas - 150) + 940
                elif sumaAlas == 160:
                    peso1 = 1000
                elif sumaAlas < 180:
                    peso1 = (1125 - 1000) / (180 - 160) * (sumaAlas - 160) + 1000
                elif sumaAlas == 180:
                    peso1 = 1125
                elif sumaAlas < 200:
                    peso1 = (1250 - 1125) / (200 - 180) * (sumaAlas - 180) + 1125
                elif sumaAlas == 200:
                    peso1 = 1250
                peso1 = int(peso1 * record.grosor_2)
                peso1 = peso1 / 10000
                
            #Perfil U
            elif record.type_id.is_perfilu == True:
                sumaAlas = record.ala_1 + record.ancho + record.ala_2 + record.grosor_2 * 2
                if sumaAlas == 60:
                    peso1 = 385
                elif sumaAlas < 66:
                    peso1 = (425 - 385) / (66 - 60) * (sumaAlas - 60) + 385
                elif sumaAlas == 66:
                    peso1 = 425
                elif sumaAlas < 70:
                    peso1 = (450 - 425) / (70 - 66) * (sumaAlas - 66) + 425
                elif sumaAlas == 70:
                    peso1 = 450
                elif sumaAlas < 76:
                    peso1 = (510 - 450) / (76 - 70) * (sumaAlas - 70) + 450
                elif sumaAlas == 76:
                    peso1 = 510
                elif sumaAlas < 80:
                    peso1 = (535 - 510) / (80 - 76) * (sumaAlas - 76) + 510
                elif sumaAlas == 80:
                    peso1 = 535
                elif sumaAlas < 84:
                    peso1 = (560 - 535) / (84 - 80) * (sumaAlas - 80) + 535
                elif sumaAlas == 84:
                    peso1 = 560
                elif sumaAlas < 90:
                    peso1 = (600 - 560) / (90 - 84) * (sumaAlas - 84) + 560
                elif sumaAlas == 90:
                    peso1 = 600
                elif sumaAlas < 100:
                    peso1 = (700 - 600) / (100 - 90) * (sumaAlas - 90) + 600
                elif sumaAlas == 100:
                    peso1 = 700
                elif sumaAlas < 120:
                    peso1 = (835 - 700) / (120 - 100) * (sumaAlas - 100) + 700
                elif sumaAlas == 120:
                    peso1 = 835
                elif sumaAlas < 140:
                    peso1 = (875 - 835) / (140 - 120) * (sumaAlas - 120) + 835
                elif sumaAlas == 140:
                    peso1 = 875
                elif sumaAlas < 150:
                    peso1 = (940 - 875) / (150 - 140) * (sumaAlas - 140) + 875
                elif sumaAlas == 150:
                    peso1 = 940
                elif sumaAlas < 160:
                    peso1 = (1000 - 940) / (160 - 150) * (sumaAlas - 150) + 940
                elif sumaAlas == 160:
                    peso1 = 1000
                elif sumaAlas < 180:
                    peso1 = (1125 - 1000) / (180 - 160) * (sumaAlas - 160) + 1000
                elif sumaAlas == 180:
                    peso1 = 1125
                elif sumaAlas < 200:
                    peso1 = (1250 - 1125) / (200 - 180) * (sumaAlas - 180) + 1125
                elif sumaAlas == 200:
                    peso1 = 1250
                #Añadido
                elif sumaAlas <= 240:
                    peso1 = (1250 - 1125) / (200 - 180) * (sumaAlas - 180) + 1125
                peso1 = int(peso1 * record.grosor_2)
                peso1 = peso1 / 10000
                
            #Slip Sheet
            elif record.type_id.is_slipsheet == True:
                peso1 = int((record.grosor_1 * 1000 / 1.4 + 30) / 50) * 50
                peso1 = peso1 / 1000
                
            #Solid Board
            elif record.type_id.is_solidboard == True:
                peso1 = int((record.grosor_1 * 1000 / 1.4 + 30) / 50) * 50
                peso1 = peso1 / 1000
                
            #Formato
            elif record.type_id.is_formato == True:
                peso1 = record.gramaje / 1000
                
            #Bobina
            elif record.type_id.is_bobina == True:
                peso1 = record.gramaje / 1000
                
            #Pie de Pallet
            elif record.type_id.is_pieballet == True:
                if record.pie == '1' or record.pie == '2':
                    peso1 = 1.25
                elif record.pie == '3' or record.pie == '4':
                    peso1 = 0.75
                        
            record.peso_metro = peso1
    
    
    
    @api.depends('type_id',)
    def _get_valores_referencia(self):
    
        for record in self:
            metros = 0
            gram = 0
            interior = 0
            superficie = 0

            #Varios
            if record.type_id.is_varios == True:
                metros = record.metros_unidad_user
            #Cantonera
            elif record.type_id.is_cantonera == True:
                metros = record.longitud / 1000
                gram = int((record.grosor_2 * 1000 / 1.4 - 300) / 50) * 50
                interior = int(record.ala_1 + record.ala_2 - record.grosor_2 * 2 - 1)
                superficie = int(((record.ala_1 + record.ala_2 - record.grosor_2 - 1) * 2 + 5) / 5) * 5
                if superficie > 280:
                    superficie = 280
            #Perfil U
            elif record.type_id.is_perfilu == True:
                metros = record.longitud / 1000
                gram = int((record.grosor_2 * 1000 / 1.4 - 300) / 50) * 50
                interior = int(record.ala_1 + record.ancho + record.ala_2 - 1)
                superficie = int(((record.ala_1 + record.ancho + record.ala_2 - 1 + record.grosor_2) * 2 + 5) / 5) * 5
                if superficie > 280:
                    superficie = 280
            #Slip Sheets
            elif record.type_id.is_slipsheet == True:
                sumaAncho = record.ancho
                if record.ala_1 > 0:
                    sumaAncho = sumaAncho + record.ala_1
                if record.ala_2 > 0:
                    sumaAncho = sumaAncho + record.ala_2
                sumaLargo = record.longitud
                if record.ala_3 > 0:
                    sumaLargo = sumaLargo + record.ala_3
                if record.ala_4 > 0:
                    sumaLargo = sumaLargo + record.ala_4
                metros = sumaAncho * sumaLargo / 1000000
                gram = int((record.grosor_1 * 1000 / 1.4 - 300) / 50) * 50
                interior = record.ancho
                if record.ala_1 != None and record.ala_1 > 0:
                    interior = interior + record.ala_1
                if record.ala_2 != None and record.ala_2 > 0:
                    interior = interior + record.ala_2
            #Solid Board
            elif record.type_id.is_solidboard == True:
                metros = record.ancho * record.longitud / 1000000
                gram = int((record.grosor_1 * 1000 / 1.4 - 300) / 50) * 50
                interior = record.ancho + 30
            #Formato
            elif record.type_id.is_formato == True:
                metros = record.ancho * record.longitud / 1000000
                gram = record.gramaje
                interior = record.ancho
            #Bobina
            elif record.type_id.is_bobina == True:
                metros = (record.diametro * record.diametro - 10000) * 0.61 / record.gramaje
                gram = record.gramaje
                interior = record.ancho
                
            #Pie de Pallet
            elif record.type_id.is_pieballet == True:
                metros = record.longitud / 1000
        
        
            record.metros_unidad = metros
            record.j_gram = gram
            record.j_interior = interior
            record.j_superficie = superficie
    
    
    @api.multi
    def create_bom_from_ref(self, bomref):
        for bom in self.env['mrp.bom'].search([('code', '=', bomref),]):
            newbom = bom.copy()
            newbom.code = ''
            newbom.product_tmpl_id = self.id
            break
            

    

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    und_pallet = fields.Integer('Unidades pallet', readonly=True)
    attribute_id = fields.Many2one('sale.product.attribute', string="Atributo producto", readonly=True, )
    referencia_cliente_id = fields.Many2one('sale.referencia.cliente', string='Referencia cliente', store=True, related='attribute_id.referencia_cliente_id')
    referencia_id = fields.Many2one('product.referencia', string='Referencia', store=True, related='attribute_id.referencia_cliente_id.referencia_id')

    
    
class ProductCategory(models.Model):
    _inherit = 'product.category'
    
    product_type = fields.Boolean('¿Es un tipo de producto?')
    is_cantonera = fields.Boolean('¿Es Cantonera?')
    is_perfilu = fields.Boolean('¿Es Perfil U?')
    is_slipsheet = fields.Boolean('¿Es Slip Sheet?')
    is_solidboard = fields.Boolean('¿Es Solid Board?')
    is_formato = fields.Boolean('¿Es Formato?')
    is_bobina = fields.Boolean('¿Es Bobina?')
    is_pieballet = fields.Boolean('¿Es Pie de Ballet?')
    is_varios = fields.Boolean('¿Es Varios?')

    
    
    @api.multi
    def create_prod_cantonera(self, ala1, ala2, grosor_2, longitud):
        if ala1 < 20 or ala1 > 120:
            return None, "Error: Ala1 debe estar entre 20 y 120"
        if ala2 < 20 or ala2 > 120:
            return None, "Error: Ala2 debe estar entre 20 y 120"
        if grosor_2 < 1.5 or grosor_2 > 8:
            return None, "Error: Grosor debe estar entre 1.5 y 8"
        if longitud < 50 or longitud > 7000:
            return None, "Error: Logitud debe estar entre 50 y 7000"
            
        sumaAlas = ala1 + ala2
        if sumaAlas < 60 or sumaAlas > 200:
             return None, "Error: La suma de las alas debe estar entre 60 y 200"
        if grosor_2 >= 7 and sumaAlas < 140:
            return None, "El grosor no puede ser superior a 7 si la suma de las alas es inferior a 140"
        if grosor_2 >= 6 and sumaAlas < 100:
            return None, "El grosor no puede ser superior a 6 si la suma de las alas es inferior a 100"
        if grosor_2 >= 5 and sumaAlas < 70:
            return None, "El grosor no puede ser superior a 5 si la suma de las alas es inferior a 70"
        if ala1 > longitud:
            return None, "Error: Ala1 no puede ser superior a la longitud"
        if ala2 > longitud:
            return None, "Error: Ala2 no puede ser superior a la longitud"
            
        if ala2 > ala1:
            aux = ala1
            ala1 = ala2
            ala2 = ala1

        if ala2 * 2 < ala1:
            return None, "Error: Ala2 * 2 debe ser menor que Ala1"
            
        #Buscamos
        for prod in self.env['product.referencia'].search([('type_id', '=', self.id), ('ala_1', '=', ala1), ('ala_2', '=', ala2), ('grosor', '=', grosor_2), ('longitud', '=', longitud)]):
            return prod, None
            

        
        product_name = "CANTONERA " + str(ala1) + " x " + str(ala2) + " x " + str(grosor_2) + " x " + str(longitud)
        
        referencia_id = self.env['product.referencia'].create({'name': product_name, 
                                                          'type_id': self.id, 
                                                          'ala_1': ala1,
                                                          'ala_2': ala2,
                                                          'grosor_2': grosor_2,
                                                          'longitud': longitud,
                                                         })
        #product_id.create_bom_from_ref("TEMPLATE CANTONERA")

        #Buscamos TEMPLATE CANTONERA
        return referencia_id, None
        
        
        
        
    @api.multi
    def create_prod_perfilu(self, ala1, ancho, ala2, grosor_2, longitud):
        if ala1 < 18 or ala1 > 70:
            return None, "Error: Ala1 debe estar entre 18 y 70"
        if ancho < 16 or ancho > 125:
            return None, "Error: ancho debe estar entre 16 y 125"
        if ala2 < 18 or ala2 > 70:
            return None, "Error: Ala2 debe estar entre 18 y 70"
        if grosor_2 < 2 or grosor_2 > 5.5:
            return None, "Error: Grosor debe estar entre 2 y 5.5"
        if longitud < 400 or longitud > 6000:
            return None, "Error: Logitud debe estar entre 400 y 6000"
            
        sumaAlas = ala1 + ala2
        if sumaAlas < 60 or sumaAlas > 240:
             return None, "Error: La suma de las alas debe estar entre 60 y 240"
        
        if ala2 > ala1:
            aux = ala1
            ala1 = ala2
            ala2 = ala1

        #Buscamos
        for prod in self.env['product.referencia'].search([('type_id', '=', self.id), ('ala_1', '=', ala1), ('ancho', '=', ancho), ('ala_2', '=', ala2), ('grosor_2', '=', grosor_2), ('longitud', '=', longitud)]):
            return prod, None
            
            
        
        

        product_name = "PERFIL U " + str(ala1) + " x " + str(ancho) + " x "  + str(ala2) + " x " + str(grosor_2) + " x " + str(longitud)
        
        referencia_id = self.env['product.referencia'].create({'name': product_name, 
                                                          'type_id': self.id, 
                                                          'ala_1': ala1,
                                                          'ancho': ancho,
                                                          'ala_2': ala2,
                                                          'grosor_2': grosor_2,
                                                          'longitud': longitud,
                                                         })
        
        return referencia_id, None
        
        
    @api.multi
    def create_prod_slipsheet(self, ala1, ancho, ala2, grosor_1, longitud, ala3, ala4):
    
        sumaAncho = ancho
        if ala1 > 0:
            sumaAncho = sumaAncho + ala1
        if ala2 > 0:
            sumaAncho = sumaAncho + ala2
            
        sumaLargo = longitud
        if ala3 > 0:
            sumaLargo = sumaLargo + ala3
        if ala4 > 0:
            sumaLargo = sumaLargo + ala4
            
    
        if sumaAncho < 500 or sumaAncho > 1200:
            return None, "Error: (Ala_1 + Ancho + Ala_2) debe estar entre 500 y 1200"
        if sumaLargo < 500 or sumaLargo > 1600:
            return None, "Error: (Ala_3 + Longitud + Ala_4) debe estar entre 500 y 1600"
        if grosor_1 < 0.6 or grosor_1 > 4.0:
            return None, "Error: Grosor debe estar entre 0.6 y 4.0"
            

        #Buscamos
        for prod in self.env['product.referencia'].search([('type_id', '=', self.id), ('ala_1', '=', ala1), ('ancho', '=', ancho), ('ala_2', '=', ala2), ('grosor_1', '=', grosor_1), ('longitud', '=', longitud), ('ala_3', '=', ala3), ('ala_4', '=', ala4),]):
            return prod, None
            
            
        

        product_name = "SLIP SHEET ("
        if ala1 > 0:
            product_name = product_name + str(ala1) + " + "
        product_name = product_name + str(ancho)
        if ala2 > 0:
            product_name = product_name + " + " + str(ala2)
        product_name = product_name + ") x ("
        if ala3 > 0:
            product_name = product_name + str(ala3) + " + "
        product_name = product_name + str(longitud)
        if ala4 > 0:
            product_name = product_name + " + " + str(ala4)
        product_name = product_name + ") x " + str(grosor_1)
        
        referencia_id = self.env['product.referencia'].create({'name': product_name, 
                                                          'type_id': self.id, 
                                                          'ala_1': ala1,
                                                          'ancho': ancho,
                                                          'ala_2': ala2,
                                                          'ala_3': ala3,
                                                          'ala_4': ala4,
                                                          'grosor_1': grosor_1,
                                                          'longitud': longitud,
                                                         })

        return referencia_id, None
        
        
    @api.multi
    def create_prod_solidboard(self, ancho, grosor_1, longitud):
    
    
        if ancho < 50 or ancho > 1200:
            return None, "Error: ancho debe estar entre 50 y 1200"
        if longitud < 500 or longitud > 1600:
            return None, "Error: Longitud debe estar entre 500 y 1600"
        if grosor_1 < 0.6 or grosor_1 > 5.5:
            return None, "Error: Grosor debe estar entre 0.6 y 5.5"
            

        #Buscamos
        for prod in self.env['product.referencia'].search([('type_id', '=', self.id), ('ancho', '=', ancho), ('grosor_1', '=', grosor_1), ('longitud', '=', longitud), ]):
            return prod, None


        product_name = "SOLID BOARD " + str(ancho) + " x " + str(longitud) + " x " + str(grosor_1)
            
        referencia_id = self.env['product.referencia'].create({'name': product_name, 
                                                          'type_id': self.id, 
                                                          'ancho': ancho,
                                                          'grosor_1': grosor_1,
                                                          'longitud': longitud,
                                                         })

        return referencia_id, None
        
        
        
    @api.multi
    def create_prod_formato(self, ancho, longitud, gramaje):
    
    
        if ancho < 500 or ancho > 1400:
            return None, "Error: ancho debe estar entre 500 y 1400"
        if longitud < 500 or longitud > 1800:
            return None, "Error: Longitud debe estar entre 500 y 1800"
            

        #Buscamos
        for prod in self.env['product.referencia'].search([('type_id', '=', self.id), ('ancho', '=', ancho), ('longitud', '=', longitud), ('gramaje', '=', gramaje), ]):
            return prod, None


        product_name = "FORMATO " + str(ancho) + " x " + str(longitud) + " - " + str(gramaje) + "g"
            
        referencia_id = self.env['product.referencia'].create({'name': product_name, 
                                                          'type_id': self.id, 
                                                          'ancho': ancho,
                                                          'longitud': longitud,
                                                          'gramaje': gramaje,
                                                         })

        return referencia_id, None
        
        
    @api.multi
    def create_prod_bobina(self, ancho, diametro, gramaje):
    
    
        if ancho < 20 or ancho > 2800:
            return None, "Error: ancho debe estar entre 20 y 2800"
        if diametro < 300 or diametro > 1400:
            return None, "Error: Diámetro debe estar entre 300 y 1400"
            

        #Buscamos
        for prod in self.env['product.referencia'].search([('type_id', '=', self.id), ('ancho', '=', ancho), ('diametro', '=', diametro), ('gramaje', '=', gramaje), ]):
            return prod, None


        product_name = "BOBINA Ancho " + str(ancho) + "mm - Ø " + str(diametro) + " - " + str(gramaje) + "g"
            
        referencia_id = self.env['product.referencia'].create({'name': product_name, 
                                                          'type_id': self.id, 
                                                          'ancho': ancho,
                                                          'diametro': diametro,
                                                          'gramaje': gramaje,
                                                         })

        return referencia_id, None
        
        
    @api.multi
    def create_prod_pieballet(self, longitud, pie):
    
    
        if longitud < 190 or longitud > 1800:
            return None, "Error: Longitud debe estar entre 190 y 1800"
            

        #Buscamos
        for prod in self.env['product.referencia'].search([('type_id', '=', self.id), ('longitud', '=', longitud), ('pie', '=', pie), ]):
            return prod, None

        
        product_name = ""
        if pie == '1':
            product_name = "PIE DE BALLET 100 x 90 x " + str(longitud) + " - Adhesivo"
        elif pie == '2':
            product_name = "PIE DE BALLET 100 x 90 x " + str(longitud)
        elif pie == '3':
            product_name = "PIE DE BALLET 60 x 90 x " + str(longitud) + " - Adhesivo"
        elif pie == '4':
            product_name = "PIE DE BALLET 60 x 90 x " + str(longitud)        
            
        referencia_id = self.env['product.referencia'].create({'name': product_name, 
                                                          'type_id': self.id, 
                                                          'longitud': longitud,
                                                          'pie': pie,
                                                         })

        return referencia_id, None
    
         
        
    
    

###############################
# CARACTERISTICAS REF CLIENTE #
###############################    

class ProductCaracteristicaPalletEspecial(models.Model):
    _name = 'product.caracteristica.pallet.especial'
    _order = 'number'
    
    name = fields.Char('Nombre', required=True)
    number = fields.Integer('Número', required=True)
    active = fields.Boolean('Activo', default=True)
    description = fields.Char('Descripción')
    incremento = fields.Float('Incremento', digits=(8, 4), required = True)
    
    TIPO_SEL = [('1', 'Metro de Producto'), 
               ('2', 'Unidad de Producto'),
               ('3', 'Porcentaje de Producto'),                 
               ('4', 'Por Pallet'),
               ]
    tipo = fields.Selection(selection = TIPO_SEL, string = 'Tipo')
    


############################
# CARACTERISTICAS ATRIBUTO #
############################  

## CANTONERA ##



class ProductCaracteristicaCantoneraColor(models.Model):
    _name = 'product.caracteristica.cantonera.color'
    _order = 'number'
    
    name = fields.Char('Nombre', required=True)
    number = fields.Integer('Número', required=True)
    description = fields.Char('Descripción')
    
    active = fields.Boolean('Activo', default = True)
    valido = fields.Boolean('Valido para Fabricar', default = False)

    incremento = fields.Float('Incremento', digits=(8, 4), default = 0, required = True)
    TIPO_SEL = [('1', 'Metro de Producto'),   
                ('2', 'Unidad de Producto'),
                ('3', 'Porcentaje de Producto'),
                ('4', 'Por Pallet'),
                ]
    tipo = fields.Selection(selection = TIPO_SEL, string = 'Tipo', required = True)
    
    
    
class ProductCaracteristicaCantoneraForma(models.Model):
    _name = 'product.caracteristica.cantonera.forma'
    _order = 'number'
    
    name = fields.Char('Nombre', required=True)
    number = fields.Integer('Número', required=True)
    description = fields.Char('Descripción')
    active = fields.Boolean('Activo', default = True)
    incremento = fields.Float('Incremento', digits=(8, 4), default = 0, required = True)
    TIPO_SEL = [('1', 'Metro de Producto'),   
                ('2', 'Unidad de Producto'),
                ('3','Porcentaje de Producto'),
                ('4', 'Por Pallet'),
                ]
    tipo = fields.Selection(selection = TIPO_SEL, string = 'Tipo', required = True)
    cantonera_1 = fields.Boolean('Cantonera 1', default = False)
    cantonera_2 = fields.Boolean('Cantonera 2', default = False)
    cantonera_3 = fields.Boolean('Cantonera 3', default = False)
    cantonera_4 = fields.Boolean('Cantonera 4', default = False)



class ProductCaracteristicaCantoneraEspecial(models.Model):
    _name = 'product.caracteristica.cantonera.especial'
    _order = 'number'
    
    name = fields.Char('Nombre', required=True)
    number = fields.Integer('Número', required=True)
    description = fields.Char('Descripción')
    active = fields.Boolean('Activo', default = True)
    incremento = fields.Float('Incremento', digits=(8, 4), required = True)
    TIPO_SEL = [('1', 'Metro de Producto'),   
                ('2', 'Unidad de Producto'),
                ('3', 'Porcentaje de Producto'),
                ('4', 'Por Pallet'),
                ]
    tipo = fields.Selection(selection = TIPO_SEL, string = 'Tipo', required = True)
    cantonera_1 = fields.Boolean('Cantonera 1', default = False)
    cantonera_2 = fields.Boolean('Cantonera 2', default = False)
    cantonera_3 = fields.Boolean('Cantonera 3', default = False)
    cantonera_4 = fields.Boolean('Cantonera 4', default = False)



class ProductCaracteristicaCantoneraImpresion(models.Model):
    _name = 'product.caracteristica.cantonera.impresion'
    _order = 'number'
    
    name = fields.Char('Nombre', required=True)
    number = fields.Integer('Número', required=True)
    description = fields.Char('Descripción')
    active = fields.Boolean('Activo', default = True)
    num_tintas = fields.Integer('Numero de Tintas')
    incremento = fields.Float('Incremento', digits=(8, 4), required = True)
    TIPO_SEL = [('1', 'Metro de Producto'),   
                ('2', 'Unidad de Producto'),
                ('3', 'Porcentaje de Producto'),
                ('4', 'Por Pallet'),
                ]
    tipo = fields.Selection(selection = TIPO_SEL, string = 'Tipo', required = True)
    cantonera_1 = fields.Boolean('Cantonera 1', default = False)
    cantonera_2 = fields.Boolean('Cantonera 2', default = False)
    cantonera_3 = fields.Boolean('Cantonera 3', default = False)
    cantonera_4 = fields.Boolean('Cantonera 4', default = False)


## PERFILU ##


class ProductCaracteristicaPerfiluColor(models.Model):
    _name = 'product.caracteristica.perfilu.color'
    _order = 'number'
    
    name = fields.Char('Nombre', required=True)
    number = fields.Integer('Número', required=True)
    description = fields.Char('Descripción')
    
    active = fields.Boolean('Activo', default = True)
    valido = fields.Boolean('Valido para Fabricar', default = False)
    incremento = fields.Float('Incremento', digits=(8, 4), default = 0, required = True)
    TIPO_SEL = [('1', 'Metro de Producto'),   
                ('2', 'Unidad de Producto'),
                ('3', 'Porcentaje de Producto'),
                ('4', 'Por Pallet'),
                ]
    tipo = fields.Selection(selection = TIPO_SEL, string = 'Tipo', required = True)
    


## TODOS ##        
    
class ProductCaracteristicaReciclable(models.Model):
    _name = 'product.caracteristica.reciclable'
    _order = 'number'
    
    name = fields.Char('Nombre', required=True)
    number = fields.Integer('Número', required=True)
    description = fields.Char('Descripción')
    active = fields.Boolean('Activo', default = True)
    incremento = fields.Float('Incremento', digits=(8, 4), required = True)
    TIPO_SEL = [('1', 'Metro de Producto'),   
                ('2', 'Unidad de Producto'),
                ('3', 'Porcentaje de Producto'),
                ('4', 'Por Pallet'),
                ]
    tipo = fields.Selection(selection = TIPO_SEL, string = 'Tipo', required = True)
    cantonera_1 = fields.Boolean('Cantonera 1', default = False)
    cantonera_2 = fields.Boolean('Cantonera 2', default = False)
    cantonera_3 = fields.Boolean('Cantonera 3', default = False)
    cantonera_4 = fields.Boolean('Cantonera 4', default = False)
    
    
class ProductCaracteristicaFSC(models.Model):
    _name = 'product.caracteristica.fsc'
    _order = 'number'
    
    name = fields.Char('Nombre', required=True)
    number = fields.Integer('Número', required=True)
    description = fields.Char('Descripción')
    active = fields.Boolean('Activo', default = True)
    incremento = fields.Float('Incremento', digits=(8, 4), required = True)
    TIPO_SEL = [('1', 'Metro de Producto'),   
                ('2', 'Unidad de Producto'),
                ('3', 'Porcentaje de Producto'),
                ('4', 'Por Pallet'),
                ]
    tipo = fields.Selection(selection = TIPO_SEL, string = 'Tipo', required = True)
    cantonera_1 = fields.Boolean('Cantonera 1', default = False)
    cantonera_2 = fields.Boolean('Cantonera 2', default = False)
    cantonera_3 = fields.Boolean('Cantonera 3', default = False)
    cantonera_4 = fields.Boolean('Cantonera 4', default = False)
    

class ProductCaracteristicaInglete(models.Model):
    _name = 'product.caracteristica.inglete'
    _order = 'number'
    
    name = fields.Char('Nombre', required=True)
    number = fields.Integer('Número', required=True)
    description = fields.Char('Descripción')
    active = fields.Boolean('Activo', default = True)
    
    incremento = fields.Float('Incremento', digits=(8, 4), default = 0, required = True)
    TIPO_SEL = [('1', 'Metro de Producto'),   
                ('2', 'Unidad de Producto'),
                ('3', 'Porcentaje de Producto'),
                ('4', 'Por Pallet'),
                ]
    tipo = fields.Selection(selection = TIPO_SEL, string = 'Tipo', required = True)



class ProductCaracteristicaPlanchacolor(models.Model):
    _name = 'product.caracteristica.planchacolor'
    _order = 'number'
    
    name = fields.Char('Nombre', required=True)
    number = fields.Integer('Número', required=True)
    description = fields.Char('Descripción')
    active = fields.Boolean('Activo', default = True)
    
    valido = fields.Boolean('Valido para Fabricar', default = False)
    incremento = fields.Float('Incremento', digits=(8, 4), required = True)
    TIPO_SEL = [('1', 'Metro Cuadrado de Producto'),   
                ('2', 'Unidad de Producto'),
                ('3', 'Porcentaje de Producto'),
                ('4', 'Por Pallet'),
                ]
    tipo = fields.Selection(selection = TIPO_SEL, string = 'Tipo', required = True)




    
    
class ProductCaracteristicaTroquelado(models.Model):
    _name = 'product.caracteristica.troquelado'
    _order = 'number'
    
    name = fields.Char('Nombre', required=True)
    number = fields.Integer('Número', required=True)
    description = fields.Char('Descripción')
    active = fields.Boolean('Activo', default = True)
    incremento = fields.Float('Incremento', digits=(8, 4), required = True)
    TIPO_SEL = [('1', 'Metro Cuadrado de Producto'),   
                ('2', 'Unidad de Producto'),
                ('3', 'Porcentaje de Producto'),
                ('4', 'Por Pallet'),
                ]
    tipo = fields.Selection(selection = TIPO_SEL, string = 'Tipo', required = True)
    troqueladora_1 = fields.Boolean('Troqueladora 1', default = False)
    troqueladora_2 = fields.Boolean('Troqueladora 2', default = False)
    
    
class ProductCaracteristicaPapelCalidad(models.Model):
    _name = 'product.caracteristica.papelcalidad'
    _order = 'number'
    
    name = fields.Char('Nombre', required=True)
    number = fields.Integer('Número', required=True)
    description = fields.Char('Descripción')
    active = fields.Boolean('Activo', default = True)
    incremento = fields.Float('Incremento', digits=(8, 4), required = True)
    TIPO_SEL = [('1', 'Metro Cuadrado de Producto'),   
                ('2', 'Unidad de Producto'),
                ('3', 'Porcentaje de Producto'),
                ('4', 'Por Pallet'),
                ]
    tipo = fields.Selection(selection = TIPO_SEL, string = 'Tipo', required = True)