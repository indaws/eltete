
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
    
    
    @api.multi
    def name_get(self):
        res = super(StockProductionLot, self).name_get()
        data = []
        for lot in self:
            display_value = lot.name
            if lot.unidades > 0:
                display_value = display_value + ' (' + str(lot.unidades) + ')'
            data.append((lot.id, display_value))
        return data
