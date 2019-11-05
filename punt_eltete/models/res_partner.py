
from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    
    special_conditions = fields.Text('Condiciones especiales')
    uploading_time = fields.Text('Horarios descarga')
    ice = fields.Char('ICE')
    
    prod_comment_ids = fields.One2many('partner.product.comments', 'partner_id', string="Observaciones productos")
    
    
    
class partner_product_comments(models.Model):
    _name = 'partner.product.comments'

    partner_id = fields.Many2one('res.partner', string="Cliente")
    product_id = fields.Many2one('product.template', string="Producto")
    comments = fields.Text('Comentarios')