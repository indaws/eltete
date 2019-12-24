from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

    
class tinta(models.Model):
    _name = 'mprima.tinta'

    name = fields.Char(string='Color', required = True)
    pantone = fields.Char('Pantone', required = True)
    descripcion = fields.Char('Descripción')
    active = fields.Boolean('Activa')
    
 
 
 
class tintaPallet(models.Model):
    _name = 'mprima.tinta.pallet'

    proveedor_id = fields.Many2one('proveedor', string = "Proveedor", required = True)
    fecha_entrada = fields.Date('Fecha Entrada', default=fields.Date.today(), required=True, copy=False)
    peso = fields.Float('Peso', digits=(6,1))
    
    
 
 
 
 class papel(models.Model):
    _name = 'mprima.papel'

    name = fields.Char(string='Nombre', required = True, compute="_get_name")
    TIPO_SEL = [('1', 'Fino'),
                ('2', 'Gordo'),
                ('3', 'Blanco Mate'),
                ('4', 'Blanco Brillo'
    tipo = fields.Selection(selection = TIPO_SEL, string = 'Tipo', required = True)
    calidad_id = fields.Many2one('product.caracteristica.papelcalidad', string = "Calidad")
    confsc = fields.Boolean('Con FSC')
    
    def _get_name(self):
        for record in self:
		        titulo = ""
            
            record.name = titulo

  
  


class papelPallet(models.Model):
    _name = 'mprima.papel.pallet'
    
    calidad_id = fields.Many2one('mprima.papel', string = "Papel")
    
    fecha_entrada = fields.Date('Fecha Entrada', default=fields.Date.today(), required=True, copy=False)
    proveedor_id = fields.Many2one('proveedor', string = "Proveedor", required = True)
    ref_proveedor = fields.Char('Referencia Proveedor')
    gramaje_user = fields.Date('Gramaje User', required = True)
    num_tortas = fields.Integer('Numero de Tortas', default = 1, required = True)
    peso_user = fields.Float('Peso User', digits=(6,1))
    metros_iniciales = fields.Integer('Metros Iniciales', default = 0)
    diametro = fields.Integer('Diametro', default = 0)
    
    FSC_SEL = 	[(1, 'FSC 100%'),
                (2, 'FSC MIX CREDIT'),
                (3, 'FSC MIX %'),
                (4, 'FSC RECYCLED CREDIT'),
                (5, 'FSC RECYCLED %'),
                (6, 'FSC CONTROLLED WOOD'),
                ]
    fsc_tipo = fields.Selection(selection = FSC_SEL, string = 'FSC')
    fsc_cantidad_user = fields.Integer('Porcentaje FSC', default = 0)
    
    #Calculados
    name = fields.Char('Titulo', readonly = True, compute = _get_valores())
    fsc = fields.Char('Titulo', readonly = True, compute = _get_valores())
    fsc_cantidad = fields.Float('FSC Cantidad User', readonly = True, digits=(8,2), compute = _get_valores())
    gramaje = fields.Integer('Gramaje', readonly = True, compute = _get_valores())
    
    peso = fields.Float('Peso', readonly = True, digits=(8,2), compute = _get_peso())
    metros_torta = fields.Integer('Metros Torta', readonly = True, compute = get_metros())
    
    def _get_valores(self):
        for record in self:
		        nombre = ""
            fsc = ""
            fsc_cantidad = 0
            gramaje = 0
      
            record.name = nombre
        
        
        
    def _get_peso(self):
        for record in self:
            peso = 0
      
            
            record.peso = peso
            
            
            
    def _get_metros(self):
        for record in self:
            metros = 0
      
            
            record.metros_torta = torta
    
    
    
 
   
