
from odoo import fields, models, api




class ProductPricelistOferta(models.Model):
    _name = 'product.pricelist.oferta'
    _order = 'number'
    
    number = fields.Integer('Número')
    active = fields.Boolean("Activa", default=True)
    name = fields.Char(string='Nombre', required=True)
    partner_id = fields.Many2one('res.partner', string="Solo para el Cliente")
    user_id = fields.Many2one('res.users', string="Solo para el Comercial", default=lambda self: self.env.user)
    eton = fields.Float('Eton', digits=(8,1))
    
    in_pallet_especial = fields.Boolean('Incremento Pallet Especial', default = True)
    in_fsc = fields.Boolean('Incremento FSC', default = True)
    in_reciclable = fields.Boolean('Incremento Reciclable', default = True)
    in_cantonera_color = fields.Boolean('Incremento Cantonera Color', default = True)
    in_cantonera_forma = fields.Boolean('Incremento Cantonera Forma', default = True)
    in_cantonera_especial = fields.Boolean('Incremento Cantonera Especial', default = True)
    in_cantonera_impresion = fields.Boolean('Incremento Cantonera Impresión', default = True)
    in_perfilu_color = fields.Boolean('Incremento Perfil U Color', default = True)
    in_inglete = fields.Boolean('Incremento Inglete', default = True)
    in_plancha_color = fields.Boolean('Incremento Plancha Color', default = True)
    in_papel_calidad = fields.Boolean('Incremento Papel Calidad', default = True)
    in_troquelado = fields.Boolean('Incremento Troquelado', default = True)

