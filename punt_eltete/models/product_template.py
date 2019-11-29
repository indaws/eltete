
from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    
    ala_1 = fields.Integer('Ala 1')
    base = fields.Integer('Base')
    ala_2 = fields.Integer('Ala 2')
    grosor = fields.Float('Grosor')
    longitud = fields.Integer('Longitud')
    alas = fields.Integer('Alas')
    interior = fields.Integer('Interior')
    peso = fields.Float('Peso')
    
    
    
class ProductCategory(models.Model):
    _inherit = 'product.category'
    
    product_type = fields.Boolean('¿Es un tipo de producto?')
    is_cantonera = fields.Boolean('¿Es Cantonera?')
    is_perfilu = fields.Boolean('¿Es Perfil U?')
    
    
    @api.multi
    def create_prod_cantonera(self, ala1, ala2, grosor, longitud):
        if ala1 < 20 or ala1 > 120:
            return None, "Error: Ala1 debe estar entre 20 y 120"
        if ala2 < 20 or ala2 > 120:
            return None, "Error: Ala2 debe estar entre 20 y 120"
        if grosor < 1.5 or grosor > 8:
            return None, "Error: Grosor debe estar entre 1.5 y 8"
        if longitud < 50 or longitud > 7000:
            return None, "Error: Logitud debe estar entre 50 y 7000"
            
        sumaAlas = ala1 + ala2
        if sumaAlas < 60 or sumaAlas > 200:
             return None, "Error: La suma de las alas debe estar entre 60 y 200"
        if grosor >= 7 and sumaAlas < 140:
            return None, "El grosor no puede ser superior a 7 si la suma de las alas es inferior a 140"
        if grosor >= 6 and sumaAlas < 100:
            return None, "El grosor no puede ser superior a 6 si la suma de las alas es inferior a 100"
        if grosor >= 5 and sumaAlas < 70:
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
        for prod in self.env['product.template'].search([('categ_id', '=', self.id), ('ala_1', '=', ala1), ('ala_2', '=', ala2), ('grosor', '=', grosor), ('longitud', '=', longitud)]):
            return prod, None
            
            
        interior = int(ala1 + ala2 - grosor * 2 - 1)
        peso = 0
        
        if sumaAlas == 60:
            peso = 385
        elif sumaAlas < 66:
            peso = (425 - 385) / (66 - 60) * (sumaAlas - 60) + 385
        elif sumaAlas == 66:
            peso = 425
        elif sumaAlas < 70:
            peso = (450 - 425) / (70 - 66) * (sumaAlas - 66) + 425
        elif sumaAlas == 70:
            peso = 450
        elif sumaAlas < 76:
            peso = (510 - 450) / (76 - 70) * (sumaAlas - 70) + 450
        elif sumaAlas == 76:
            peso = 510
        elif sumaAlas < 80:
            peso = (535 - 510) / (80 - 76) * (sumaAlas - 76) + 510
        elif sumaAlas == 80:
            peso = 535
        elif sumaAlas < 84:
            peso = (560 - 535) / (84 - 80) * (sumaAlas - 80) + 535
        elif sumaAlas == 84:
            peso = 560
        elif sumaAlas < 90:
            peso = (600 - 560) / (90 - 84) * (sumaAlas - 84) + 560
        elif sumaAlas == 90:
            peso = 600
        elif sumaAlas < 100:
            peso = (700 - 600) / (100 - 90) * (sumaAlas - 90) + 600
        elif sumaAlas == 100:
            peso = 700
        elif sumaAlas < 120:
            peso = (835 - 700) / (120 - 100) * (sumaAlas - 100) + 700
        elif sumaAlas == 120:
            peso = 835
        elif sumaAlas < 140:
            peso = (875 - 835) / (140 - 120) * (sumaAlas - 120) + 835
        elif sumaAlas == 140:
            peso = 875
        elif sumaAlas < 150:
            peso = (940 - 875) / (150 - 140) * (sumaAlas - 140) + 875
        elif sumaAlas == 150:
            peso = 940
        elif sumaAlas < 160:
            peso = (1000 - 940) / (160 - 150) * (sumaAlas - 150) + 940
        elif sumaAlas == 160:
            peso = 1000
        elif sumaAlas < 180:
            peso = (1125 - 1000) / (180 - 160) * (sumaAlas - 160) + 1000
        elif sumaAlas == 180:
            peso = 1125
        elif sumaAlas < 200:
            peso = (1250 - 1125) / (200 - 180) * (sumaAlas - 180) + 1125
        elif sumaAlas == 200:
            peso = 1250
            
        peso = int(peso * grosor)
        peso = peso / 10000
        
        product_name = "CANTONERA " + str(ala1) + " x " + str(ala2) + " x " + str(grosor) + " x " + str(longitud)
        
        product_id = self.env['product.template'].create({'name': product_name, 
                                                          'categ_id': self.id, 
                                                          'type':'product', 
                                                          'ala_1': ala1,
                                                          'ala_2': ala2,
                                                          'grosor': grosor,
                                                          'longitud': longitud,
                                                          'interior': interior,
                                                          'peso': peso,
                                                         })
        return product_id, None
        
        
        
        
    @api.multi
    def create_prod_perfilu(self, ala1, base, ala2, grosor, longitud):
        if ala1 < 18 or ala1 > 70:
            return None, "Error: Ala1 debe estar entre 18 y 70"
        if base < 16 or base > 125:
            return None, "Error: Base debe estar entre 16 y 125"
        if ala2 < 18 or ala2 > 70:
            return None, "Error: Ala2 debe estar entre 18 y 70"
        if grosor < 2 or grosor > 5.5:
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
        for prod in self.env['product.template'].search([('categ_id', '=', self.id), ('ala_1', '=', ala1), ('base', '=', base), ('ala_2', '=', ala2), ('grosor', '=', grosor), ('longitud', '=', longitud)]):
            return prod, None
            
            
        interior = sumaAlas
        peso = ((grosor * 1000 / 1.4 - 300) * interior / 1000 + 160 /1000 * interior * 2) / 1000
        

        product_name = "PERFIL U " + str(ala1) + " x " + str(base) + " x "  + str(ala2) + " x " + str(grosor) + " x " + str(longitud)
        
        product_id = self.env['product.template'].create({'name': product_name, 
                                                          'categ_id': self.id, 
                                                          'type':'product', 
                                                          'ala_1': ala1,
                                                          'base': base,
                                                          'ala_2': ala2,
                                                          'grosor': grosor,
                                                          'longitud': longitud,
                                                          'interior': interior,
                                                          'peso': peso,
                                                         })
        return product_id, None
         
        
    
    
class ProductCaracteristicaColor(models.Model):
    _name = 'product.caracteristica.color'
    _order = 'number'
    
    name = fields.Char('Nombre', required=True)
    number = fields.Integer('Número', required=True)
    description = fields.Char('Descripción')
    

class ProductCaracteristicaEspecial(models.Model):
    _name = 'product.caracteristica.especial'
    _order = 'number'
    
    name = fields.Char('Nombre', required=True)
    number = fields.Integer('Número', required=True)
    description = fields.Char('Descripción')
    
    
class ProductCaracteristicaAncho(models.Model):
    _name = 'product.caracteristica.ancho'
    _order = 'number'
    
    name = fields.Char('Nombre', required=True)
    number = fields.Integer('Número', required=True)
    description = fields.Char('Descripción')
    
    
    
class ProductCaracteristicaImpresion(models.Model):
    _name = 'product.caracteristica.impresion'
    _order = 'number'
    
    name = fields.Char('Nombre', required=True)
    number = fields.Integer('Número', required=True)
    description = fields.Char('Descripción')
    
    
class ProductCaracteristicaReciclable(models.Model):
    _name = 'product.caracteristica.reciclable'
    _order = 'number'
    
    name = fields.Char('Nombre', required=True)
    number = fields.Integer('Número', required=True)
    description = fields.Char('Descripción')
    
    
    
class ProductCaracteristicaPaletizado(models.Model):
    _name = 'product.caracteristica.paletizado'
    _order = 'number'
    
    name = fields.Char('Nombre', required=True)
    number = fields.Integer('Número', required=True)
    description = fields.Char('Descripción')
    
    