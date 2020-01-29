
from odoo import fields, models, api



class StockMove(models.Model):
    _inherit = 'stock.move'
    
    
    peso_neto = fields.Integer('Peso neto total', compute="_get_pesos")
    peso_bruto = fields.Integer('Peso neto total', compute="_get_pesos")
    cantidad_1_num = fields.Float('Cantidad 1', digits = (12, 4), compute="_get_pesos")
    cantidad_2_num = fields.Float('Cantidad 2', digits = (12, 4), compute="_get_pesos")
    cantidad_3_num = fields.Float('Cantidad 3', digits = (12, 4), compute="_get_pesos")
    cantidad_4_num = fields.Float('Cantidad 4', digits = (12, 4), compute="_get_pesos")
    cantidad_1 = fields.Char('Cantidad 1', compute = "_get_pesos")
    cantidad_2 = fields.Char('Cantidad 2', compute = "_get_pesos")
    cantidad_3 = fields.Char('Cantidad 3', compute = "_get_pesos")
    cantidad_4 = fields.Char('Cantidad 4', compute = "_get_pesos")
    
    @api.depends('move_line_ids')
    def _get_pesos(self):
        for record in self:
            peso_neto = 0
            peso_bruto = 0
            cantidad_1_num = 0
            cantidad_2_num = 0
            cantidad_3_num = 0
            cantidad_4_num = 0
            
            for line in record.move_line_ids:
                peso_neto = peso_neto + line.peso_neto
                peso_bruto = peso_bruto + line.peso_bruto
                cantidad_1_num = cantidad_1_num + line.cantidad_1_num
                cantidad_2_num = cantidad_2_num + line.cantidad_2_num
                cantidad_3_num = cantidad_3_num + line.cantidad_3_num
                cantidad_4_num = cantidad_4_num + line.cantidad_4_num
                
            cantidad_1_num = round(cantidad_1_num, 4)
            cantidad_2_num = round(cantidad_2_num, 4)
            cantidad_3_num = round(cantidad_3_num, 4)
            cantidad_4_num = round(cantidad_4_num, 4)
            
            cantidad_1 = str(cantidad_1_num)
            cantidad_2 = str(cantidad_2_num)
            cantidad_3 = str(cantidad_3_num)
            cantidad_4 = str(cantidad_4_num)
            
            record.peso_neto = peso_neto
            record.peso_bruto = peso_bruto
            
            record.cantidad_1_num = cantidad_1_num
            record.cantidad_2_num = cantidad_2_num
            record.cantidad_3_num = cantidad_3_num
            record.cantidad_4_num = cantidad_4_num
            
            record.cantidad_1 = cantidad_1
            record.cantidad_2 = cantidad_2
            record.cantidad_3 = cantidad_3
            record.cantidad_4 = cantidad_4
            
            #record.peso_neto = record.sale_line_id.peso_neto * record.product_uom_qty
            #record.peso_bruto = record.sale_line_id.peso_bruto * record.product_uom_qty


            
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    num_pallets = fields.Integer('Num pallets', compute="_get_num_pallets")
    
    peso_neto_total = fields.Integer('Peso neto total', compute="_get_num_pallets")
    peso_bruto_total = fields.Integer('Peso neto total', compute="_get_num_pallets")
    
    @api.depends('move_lines')
    def _get_num_pallets(self):
    
        for record in self:
            num_pallets = 0
            peso_neto_total = 0
            peso_bruto_total = 0
            for line in record.move_lines:
                if line.sale_line_id.bultos == '1':
                    num_pallets = num_pallets + int(line.product_uom_qty)
                peso_neto_total = peso_neto_total + line.peso_neto
                peso_bruto_total = peso_bruto_total + line.peso_bruto
            record.num_pallets = num_pallets
            record.peso_neto_total = peso_neto_total
            record.peso_bruto_total = peso_bruto_total
    
