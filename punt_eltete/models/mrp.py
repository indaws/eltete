from odoo import fields, models, api


class MrpProductiom(models.Model):
    _inherit = 'mrp.production'
    
    pnt_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Cliente'
    )
