
from odoo import fields, models, api




class ProductPricelistOferta(models.Model):
    _name = 'product.pricelist.oferta'
    
    
    user_id = fields.Many2one('res.users', string="Comercial", default=lambda self: self.env.user, required=True)
    activa = fields.Boolean("Activa")
    name = fields.Char(string='Nombre', required=True)
    number = fields.Integer('Incremento', required=True)
    CATEGORIA_SEL = [('1', 'General'),
                     ('2', 'Cliente'),
                     ('3', 'Comercial'),
                    ]
    categoria = fields.Selection(selection = CATEGORIA_SEL, string = 'Categoría')
    partner_id = fields.Many2one('res.partner', string="Cliente")
    eton = fields.Float('Incremento', digits=(8,1))
    porcentaje = fields.Boolean('Aplicar incremeneto Porcentaje')
    metro = fields.Boolean('Aplicar incremeneto Metro')
    unidad = fields.Boolean('Aplicar incremeneto Unidad')
    pallet = fields.Boolean('Aplicar incremeneto Pallet')
    description = fields.Char(string='Descripción')
