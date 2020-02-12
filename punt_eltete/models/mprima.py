from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

 
	
class Maquina(models.Model):
    _name = 'mprima.maquina'

    name = fields.Char(string='Nombre', required = True)
    




class Papel(models.Model):
    _name = 'mprima.papel'

    name = fields.Char(string='Nombre', required = True, compute="_get_name")
    ancho = fields.Integer('Ancho', required = True)
    gordo = fields.Boolean('¿Es Gordo?')
    confsc = fields.Boolean('¿Con FSC')    

    def _get_name(self):
        for record in self:
            nombre = "PAPEL "
	    if record.ancho > 0:
	        nombre = nombre + record.ancho
            if record.gordo == True:
		nombre = nombre + " GORDO"
            else:
		nombre = nombre + " FINO"
	    if record.confsc == True:
		nombre = nombre + " FSC"
	    else:
		nombre = nombre + " NORMAL"
			
            record.name = nombre


	
class PapelPallet(models.Model):
    _name = 'mprima.papel.pallet'

    name = fields.Char(string='Nombre', required = True)
    num_tortas = fields.Integer('Num Tortas', required = True, default = 1)
    peso = fields.Boolean('Peso', required = True)
  
 
   
