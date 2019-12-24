
from odoo import fields, models, api




class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    
    
    
    #CAMPOS REFERENCIA CLIENTE
    pallet_especial_id = fields.Many2one('product.caracteristica.pallet.especial', string = "Pallet especial")
    paletizado = fields.Integer('Paletizado')
    ancho_pallet = fields.Integer('Ancho Pallet')
    und_paquete = fields.Integer('Und Paquete')
    paquetes_fila = fields.Integer('Paquetes Fila')
    alto_fila = fields.Integer('Alto Fila')
    fila_max = fields.Integer('Fila Max')
    fila_buena = fields.Integer('Fila Buena')

    #CAMPOS OFERTA
    unidades = fields.Integer('Unidades')
    
    #OTROS
    fabricado = fields.Boolean('Fabricado')
