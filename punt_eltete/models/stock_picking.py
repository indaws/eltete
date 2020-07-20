
from odoo import fields, models, api
from odoo import exceptions


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    sale_order_line_id = fields.Many2one('sale.order.line', string = "Línea de pedido", related='move_id.sale_line_id', readonly=True)


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    peso_neto_mojado = fields.Integer('Peso neto mojado', compute="_get_pesos")
    peso_bruto_mojado = fields.Integer('Peso bruto mojado', compute="_get_pesos")
    
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
    
    
    @api.depends('move_line_ids', 'sale_line_id')
    def _get_pesos(self):
        for record in self:
            peso_neto_mojado = 0
            peso_bruto_mojado = 0
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
                if line.qty_done == 1:
                    peso_neto = peso_neto + line.lot_id.peso_neto
                    peso_bruto = peso_bruto + line.lot_id.peso_bruto
                    cantidad_1 = cantidad_1 + line.lot_id.cantidad_1_num
                    cantidad_2 = cantidad_2 + line.lot_id.cantidad_2_num
                    cantidad_3 = cantidad_3 + line.lot_id.cantidad_3_num
                    cantidad_4 = cantidad_4 + line.lot_id.cantidad_4_num
                    if line.lot_id:
                        num_pallets = num_pallets + 1
                    unidades = unidades + line.lot_id.unidades
              
            if num_pallets > 0 or record.sale_line_id.bultos == '2':
                hay_lotes = True
                
            peso_neto_mojado = int(peso_neto * 1.05 / 10) * 10
            peso_bruto_mojado = int(peso_bruto * 1.05 / 10) * 10
            
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
            
            record.peso_neto_mojado = peso_neto_mojado
            record.peso_bruto_mojado = peso_bruto_mojado



            
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    num_pallets = fields.Integer('Num pallets', compute="_get_num_pallets")
    precinto_contenedor = fields.Char('Precinto Contenedor')
    numero_contenedor = fields.Char('Número Contenedor')
    hay_contenedor = fields.Boolean('Contenedor', compute="_get_contenedor")
    transporte = fields.Char('Transporte')
    peso_neto_total = fields.Integer('Peso neto', compute="_get_num_pallets")
    peso_bruto_total = fields.Integer('Peso bruto', compute="_get_num_pallets")
    peso_neto_mojado = fields.Integer('Peso neto Mojado', compute="_get_num_pallets")
    peso_bruto_mojado = fields.Integer('Peso bruto Mojado', compute="_get_num_pallets")
    neto_mojado_user = fields.Integer('Neto User')
    bruto_mojado_user = fields.Integer('Bruto User')
    
    
    @api.multi
    def validar_asignar_albaran_compra(self):
        for record in self:
        
            #Comprobamos que todas las lineas tienen lote
            for line in record.move_ids_without_package:
                if line.purchase_line_id:
                    if line.product_uom_qty != line.purchase_line_id.num_lotes:
                        raise exceptions.ValidationError('Error: el número de lotes no coincide con el número de unidades')
                        return None
                else:
                    raise exceptions.ValidationError('Error: esta función solo se puede utilizar en albaranes generados desde pedidos de compra')
                    return None
                    
            #Asignamos líneas de fabricacion
            for line in record.move_ids_without_package:
                lista_id_lotes = []
                for lote in line.purchase_line_id.lot_ids:
                    lista_id_lotes.append(lote.id)
                i=0
                for move_line in line.move_line_ids:
                    move_line.lot_id = lista_id_lotes[i]
                    move_line.qty_done = move_line.product_uom_qty
                    i=i+1
                    
            #Validamos
            record.button_validate()
    
    
    @api.depends('precinto_contenedor')
    def _get_contenedor(self):
    
        for record in self:
            hay_contenedor = False
            if record.precinto_contenedor:
                hay_contenedor = True
                
            record.hay_contenedor = hay_contenedor
    
    @api.depends('move_lines', 'neto_mojado_user', 'bruto_mojado_user')
    def _get_num_pallets(self):
    
        for record in self:
            num_pallets = 0
            peso_neto = 0
            peso_bruto = 0
            peso_neto_mojado = 0
            peso_bruto_mojado = 0
            
            for line in record.move_lines:
                if line.product_uom_qty > 0.0:
                    if line.sale_line_id.bultos == '1':
                        num_pallets = num_pallets + line.num_pallets
                    peso_neto = peso_neto + line.peso_neto
                    peso_bruto = peso_bruto + line.peso_bruto
                    peso_neto_mojado = peso_neto_mojado + line.peso_neto_mojado
                    peso_bruto_mojado = peso_bruto_mojado + line.peso_bruto_mojado
            
            """
            if peso_neto > 0:
                divisor = 150000
                peso_neto_mojado = (1 + (peso_neto / divisor)) * peso_neto
                peso_neto_mojado = int(peso_neto_mojado / 5) * 5
                peso_bruto_mojado = (1 + (peso_bruto / divisor)) * peso_bruto
                peso_bruto_mojado = int(peso_bruto_mojado / 5) * 5
            
                if peso_bruto < 24000:
                    while peso_bruto_mojado > 24000:
                        divisor = divisor + 10000
                        peso_neto_mojado = (1 + (peso_neto / divisor)) * peso_neto
                        peso_neto_mojado = int(peso_neto_mojado / 5) * 5
                        peso_bruto_mojado = (1 + (peso_bruto / divisor)) * peso_bruto
                        peso_bruto_mojado = int(peso_bruto_mojado / 5) * 5
                    
                    if peso_neto_mojado < peso_neto:
                        peso_neto_mojado = peso_neto
                    if peso_bruto_mojado < peso_bruto:
                        peso_bruto_mojado = peso_bruto 
                else:
                    peso_neto_mojado = peso_neto
                    peso_bruto_mojado = peso_bruto
            """
            if record.neto_mojado_user > 0:
                peso_neto_mojado = record.neto_mojado_user
            if record.bruto_mojado_user > 0:
                peso_bruto_mojado = record.bruto_mojado_user   
            
            record.num_pallets = num_pallets
            record.peso_neto_total = peso_neto
            record.peso_bruto_total = peso_bruto
            record.peso_neto_mojado = peso_neto_mojado
            record.peso_bruto_mojado = peso_bruto_mojado
    
