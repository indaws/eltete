
from odoo import fields, models, api



class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    sale_order_line_id = fields.Many2one('sale.order.line', string = "Línea de pedido", related='move_id.sale_line_id', readonly=True)


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    
    peso_neto = fields.Integer('Peso neto', compute="_get_pesos")
    peso_bruto = fields.Integer('Peso bruto', compute="_get_pesos")
    cantidad_1_num = fields.Float('Cantidad 1', digits = (12, 4), compute="_get_pesos")
    cantidad_2_num = fields.Float('Cantidad 2', digits = (12, 4), compute="_get_pesos")
    cantidad_3_num = fields.Float('Cantidad 3', digits = (12, 4), compute="_get_pesos")
    cantidad_4_num = fields.Float('Cantidad 4', digits = (12, 4), compute="_get_pesos")
    cantidad_1 = fields.Char('Cantidad 1', compute = "_get_pesos")
    cantidad_2 = fields.Char('Cantidad 2', compute = "_get_pesos")
    cantidad_3 = fields.Char('Cantidad 3', compute = "_get_pesos")
    cantidad_4 = fields.Char('Cantidad 4', compute = "_get_pesos")
    num_pallets = fields.Integer('Num Pallets', compute = "_get_pesos")
    unidades = fields.Integer('Unidades', compute = "_get_pesos")
    hay_lotes = fields.Boolean('Hay Lotes', compute = "_get_pesos")
    
    orden_fabricacion = fields.Char('Orden Fabricación', compute = "_get_produccion")
    
    @api.depends('sale_line_id')
    def _get_produccion(self):
        for record in self:
            orden_fabricacion = ''
            if record.sale_line_id:
                orden_fabricacion = record.sale_line_id.orden_fabricacion
            record.orden_fabricacion = orden_fabricacion
    
    
    @api.depends('move_line_ids')
    def _get_pesos(self):
        for record in self:
            peso_neto = 0
            peso_bruto = 0
            cantidad_1 = 0
            cantidad_2 = 0
            cantidad_3 = 0
            cantidad_4 = 0
            num_pallets = 0
            unidades = 0
            hay_lotes = False
            
            for line in record.move_line_ids:
                peso_neto = peso_neto + line.lot_id.peso_neto
                peso_bruto = peso_bruto + line.lot_id.peso_bruto
                cantidad_1 = cantidad_1 + line.lot_id.cantidad_1_num
                cantidad_2 = cantidad_2 + line.lot_id.cantidad_2_num
                cantidad_3 = cantidad_3 + line.lot_id.cantidad_3_num
                cantidad_4 = cantidad_4 + line.lot_id.cantidad_4_num
                if line.lot_id:
                    num_pallets = num_pallets + 1
                unidades = unidades + line.lot_id.unidades
              
            if num_pallets > 0:
                hay_lotes = True
                
            cantidad_1 = round(cantidad_1, 4)
            cantidad_2 = round(cantidad_2, 4)
            cantidad_3 = round(cantidad_3, 4)
            cantidad_4 = round(cantidad_4, 4)
            
            record.cantidad_1_num = cantidad_1
            record.cantidad_2_num = cantidad_2
            record.cantidad_3_num = cantidad_3
            record.cantidad_4_num = cantidad_4
            
            record.cantidad_1 = str(cantidad_1)
            record.cantidad_2 = str(cantidad_2)
            record.cantidad_3 = str(cantidad_3)
            record.cantidad_4 = str(cantidad_4)
   
            record.peso_neto = peso_neto
            record.peso_bruto = peso_bruto
            record.num_pallets = num_pallets
            record.unidades = unidades
            record.hay_lotes = hay_lotes



            
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    num_pallets = fields.Integer('Num pallets', compute="_get_num_pallets")
    precinto_contenedor = fields.Char('Precinto Contenedor')
    numero_contenedor = fields.Char('Número Contenedor')
    transporte = fields.Char('Transporte')
    peso_neto_total = fields.Integer('Peso neto', compute="_get_num_pallets")
    peso_bruto_total = fields.Integer('Peso bruto', compute="_get_num_pallets")
    peso_neto_mojado = fields.Integer('Peso neto Mojado', compute="_get_num_pallets")
    peso_bruto_mojado = fields.Integer('Peso bruto Mojado', compute="_get_num_pallets")
    
    @api.depends('move_lines')
    def _get_num_pallets(self):
    
        for record in self:
            num_pallets = 0
            peso_neto_total = 0
            peso_bruto_total = 0
            for line in record.move_lines:
                if line.product_uom_qty > 0.0:
                    if line.sale_line_id.bultos == '1':
                        num_pallets = num_pallets + line.num_pallets
                    peso_neto_total = peso_neto_total + line.peso_neto
                    peso_bruto_total = peso_bruto_total + line.peso_bruto
                    
            peso_neto_mojado = (1 + (peso_neto_total / 200000)) * peso_neto_total
            peso_neto_mojado = int(peso_neto_mojado / 5) * 5
            peso_bruto_mojado = (1 + (peso_bruto_total / 200000)) * peso_bruto_total
            peso_bruto_mojado = int(peso_bruto_mojado / 5) * 5
            
            record.num_pallets = num_pallets
            record.peso_neto_total = peso_neto_total
            record.peso_bruto_total = peso_bruto_total
            record.peso_neto_mojado = peso_neto_mojado
            record.peso_bruto_mojado = peso_bruto_mojado
    
