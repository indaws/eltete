
from odoo import fields, models, api




class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    
    
    num_pallets = fields.Integer('Num pallets', compute="_get_num_pallets")
    
    @api.depends('move_lines')
    def _get_num_pallets(self):
    
        for record in self:
            num_pallets = 0
            for line in record.move_lines:
                num_pallets = num_pallets + int(line.product_uom_qty)
            record.num_pallets = num_pallets
    