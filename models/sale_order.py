
from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    
    oferta_id = fields.Many2one('sale.offer.oferta', string="Oferta")
    

