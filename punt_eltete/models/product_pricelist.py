
from odoo import fields, models, api




class ProductPricelistOferta(models.Model):
    _name = 'product.pricelist.oferta'
    _order = number
    
    active = fields.Boolean("Activa", default=True)
    name = fields.Char(string='Nombre', required=True)
    partner_id = fields.Many2one('res.partner', string="Cliente")
    user_id = fields.Many2one('res.users', string="Comercial", default=lambda self: self.env.user)
    number = fields.Integer('Incremento')
    eton = fields.Float('Incremento', digits=(8,1))
    description = fields.Char(string='Descripción')
    
    
    pallet_especial_incremento = fields.Float('Pallet Especial Incremento', digits=(12,4))
    PALLET_ESPECIAL_SEL = [('0', 'Por Defecto'),
                        ('1', 'Metro de Producto'),
                        ('2', 'Unidad de Producto'),
                        ('3', 'Porcentaje de Producto'),
                        ('4', 'Por Pallet'),
                        ]
    pallet_especial_tipo = fields.Selection(selection = PALLET_ESPECIAL_SEL, required = True, string = 'Pallet Especial Tipo', default = '0')
    
    fsc_incremento = fields.Float('FSC Incremento', digits=(12,4))
    FSC_SEL = [('0', 'Por Defecto'),
                        ('1', 'Metro de Producto'),
                        ('2', 'Unidad de Producto'),
                        ('3', 'Porcentaje de Producto'),
                        ('4', 'Por Pallet'),
                        ]
    fsc_tipo = fields.Selection(selection = FSC_SEL, required = True, string = 'FSC Tipo', default = '0')
    
    reciclable_incremento = fields.Float('Pallet Especial Incremento', digits=(12,4))
    RECICLABLE_SEL = [('0', 'Por Defecto'),
                        ('1', 'Metro de Producto'),
                        ('2', 'Unidad de Producto'),
                        ('3', 'Porcentaje de Producto'),
                        ('4', 'Por Pallet'),
                        ]
    reciclable_tipo = fields.Selection(selection = RECICLABLE_SEL, required = True, string = 'Reciclable Tipo', default = '0')
    
    cantonera_color_incremento = fields.Float('Cantonera Color Incremento', digits=(12,4))
    CANTONERA_COLOR_SEL = [('0', 'Por Defecto'),
                        ('1', 'Metro de Producto'),
                        ('2', 'Unidad de Producto'),
                        ('3', 'Porcentaje de Producto'),
                        ('4', 'Por Pallet'),
                        ]
    cantonera_color_tipo = fields.Selection(selection = CANTONERA_COLOR_SEL, required = True, string = 'Cantonera Color Tipo', default = '0')
    
    cantonera_forma_incremento = fields.Float('Cantonera Forma Incremento', digits=(12,4))
    CANTONERA_FORMA_SEL = [('0', 'Por Defecto'),
                        ('1', 'Metro de Producto'),
                        ('2', 'Unidad de Producto'),
                        ('3', 'Porcentaje de Producto'),
                        ('4', 'Por Pallet'),
                        ]
    cantonera_forma_tipo = fields.Selection(selection = CANTONERA_FORMA_SEL, required = True, string = 'Cantonera Forma Tipo', default = '0')
    
    cantonera_especial_incremento = fields.Float('Pallet Especial Incremento', digits=(12,4))
    CANTONERA_ESPECIAL_SEL = [('0', 'Por Defecto'),
                        ('1', 'Metro de Producto'),
                        ('2', 'Unidad de Producto'),
                        ('3', 'Porcentaje de Producto'),
                        ('4', 'Por Pallet'),
                        ]
    cantonera_especial_tipo = fields.Selection(selection = CANTONERA_ESPECIAL_SEL, required = True, string = 'Cantonera Especial Tipo', default = '0')
    
    cantonera_impresion_incremento = fields.Float('Pallet Impresión Incremento', digits=(12,4))
    CANTONERA_IMPRESION_SEL = [('0', 'Por Defecto'),
                        ('1', 'Metro de Producto'),
                        ('2', 'Unidad de Producto'),
                        ('3', 'Porcentaje de Producto'),
                        ('4', 'Por Pallet'),
                        ]
    cantonera_impresion_tipo = fields.Selection(selection = CANTONERA_IMPRESION_SEL, required = True, string = 'Cantonera Impresión Tipo', default = '0')
    
    perfilu_color_incremento = fields.Float('Perfil U Color Incremento', digits=(12,4))
    PERFILU_COLOR_SEL = [('0', 'Por Defecto'),
                        ('1', 'Metro de Producto'),
                        ('2', 'Unidad de Producto'),
                        ('3', 'Porcentaje de Producto'),
                        ('4', 'Por Pallet'),
                        ]
    perfilu_color_tipo = fields.Selection(selection = PERFILU_COLOR_SEL, required = True, string = 'Perfil U Color Tipo', default = '0')
    
    inglete_incremento = fields.Float('Inglete Incremento', digits=(12,4))
    INGLETE_SEL = [('0', 'Por Defecto'),
                        ('1', 'Metro de Producto'),
                        ('2', 'Unidad de Producto'),
                        ('3', 'Porcentaje de Producto'),
                        ('4', 'Por Pallet'),
                        ]
    inglete_tipo = fields.Selection(selection = INGLETE_SEL, required = True, string = 'Inglete Tipo', default = '0')
    
    plancha_color_incremento = fields.Float('Plancha Color Incremento', digits=(12,4))
    PLANCHA_COLOR_SEL = [('0', 'Por Defecto'),
                        ('1', 'Metro de Producto'),
                        ('2', 'Unidad de Producto'),
                        ('3', 'Porcentaje de Producto'),
                        ('4', 'Por Pallet'),
                        ]
    plancha_color_tipo = fields.Selection(selection = PLANCHA_COLOR_SEL, required = True, string = 'Plancha Color Tipo', default = '0')
    
    papel_calidad_incremento = fields.Float('Papel Calidad Incremento', digits=(12,4))
    PAPEL_CALIDAD_SEL = [('0', 'Por Defecto'),
                        ('1', 'Metro de Producto'),
                        ('2', 'Unidad de Producto'),
                        ('3', 'Porcentaje de Producto'),
                        ('4', 'Por Pallet'),
                        ]
    papel_calidad_tipo = fields.Selection(selection = PAPEL_CALIDAD_SEL, required = True, string = 'Papel Calidad Tipo', default = '0')
    
    troquelado_incremento = fields.Float('Troquelado Incremento', digits=(12,4))
    TROQUELADO_SEL = [('0', 'Por Defecto'),
                        ('1', 'Metro de Producto'),
                        ('2', 'Unidad de Producto'),
                        ('3', 'Porcentaje de Producto'),
                        ('4', 'Por Pallet'),
                        ]
    troquelado_tipo = fields.Selection(selection = TROQUELADO_SEL, required = True, string = 'Troquelado Tipo', default = '0')
    
    
    #ELIMINAR
    CATEGORIA_SEL = [('1', 'General'),
                     ('2', 'Cliente'),
                     ('3', 'Comercial'),
                    ]
    categoria = fields.Selection(selection = CATEGORIA_SEL, string = 'Categoría')
    porcentaje = fields.Boolean('Aplicar incremeneto Porcentaje')
    metro = fields.Boolean('Aplicar incremeneto Metro')
    unidad = fields.Boolean('Aplicar incremeneto Unidad')
    pallet = fields.Boolean('Aplicar incremeneto Pallet')

    
    
