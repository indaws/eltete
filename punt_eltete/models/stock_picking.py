
from odoo import fields, models, api



class StockMove(models.Model):
    _inherit = 'stock.move'
    
    
    peso_neto = fields.Integer('Peso neto total', compute="_get_pesos")
    peso_bruto = fields.Integer('Peso neto total', compute="_get_pesos")
    
    @api.depends('move_line_ids')
    def _get_pesos(self):
        for record in self:
            
            for line in record.move_line_ids:
                peso_neto = line.peso_neto
            
            
            record.peso_neto = record.sale_line_id.peso_neto * record.product_uom_qty
            record.peso_bruto = record.sale_line_id.peso_bruto * record.product_uom_qty


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
    
