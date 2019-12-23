
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

    
class sale_cotizacion(models.Model):
    _name = 'sale.cotizacion'

    name = fields.Char(string='Cotización', required=True, copy=False, readonly=True, index=True, default=lambda self: "/")
    
    partner_id = fields.Many2one('res.partner', string="Cliente", required=True)
    user_id = fields.Many2one('res.users', string="Comercial", default=lambda self: self.env.user, required=True)
    date = fields.Date('Fecha', default=fields.Date.today(), required=True)
    state_id = fields.Many2one('res.country.state', string="Provincia")
    country_id = fields.Many2one('res.country', string="País")
    
    line_ids = fields.One2many('sale.cotizacion.line', 'cotizacion_id', string="Líneas")
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sale.cotizacion'
                )
        return super().create(vals_list)
    
    
    
    
    
    
class sale_presupuesto_line(models.Model):
    _name = 'sale.cotizacion.line'
    
    sequence = fields.Integer('Secuencia')
    cotizacion_id = fields.Many2one('sale.cotizacion', string="Presupuesto", required=True, readonly=True, ondelete='cascade')
    referencia_cliente_id = fields.Many2one('sale.referencia.cliente', string='Referencia cliente', required=True, readonly=True)
    attribute_id = fields.Many2one('sale.product.attribute', string="Atributo producto", required=True, readonly=True)
    oferta_id = fields.Many2one('sale.offer.oferta', string="Oferta", required=True, readonly=True)
    cantonera_impresion_id = fields.Many2one('product.caracteristica.cantonera.impresion', string="Impresión")
    reciclable_id = fields.Many2one('product.caracteristica.reciclable', string = "Reciclable")
    und_pallet = fields.Integer('Unidades pallet', readonly=True)
    npallets = fields.Integer('Num pallets', readonly=True)
    emetro = fields.Float('Emetro', readonly=True)
    eton = fields.Float('Eton', readonly=True)
    
    
    
    
    
    
    
    
    

class WizardSaleCotizacion(models.TransientModel):
    _name = 'wizard.sale.cotizacion'
    _description = "Añadir ofertas a la cotización"
    
    def _default_cotizacion(self):
        return self.env['sale.cotizacion'].browse(self._context.get('active_id'))
        
    def _default_partner(self):
        return self.env['sale.cotizacion'].browse(self._context.get('active_id')).partner_id
    
    cotizacion_id = fields.Many2one('sale.cotizacion', string="Cotización", required=True, default=_default_cotizacion, readonly=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string="Cliente", required=True, default=_default_partner, readonly=True)
    
    referencia_cliente_id = fields.Many2one('sale.referencia.cliente', string='Referencia cliente', required=True)
    attribute_id = fields.Many2one('sale.product.attribute', string="Atributo producto", required=True)
    oferta_ids = fields.Many2many('sale.offer.oferta', string="Ofertas de la referencia", required=True)
    

    @api.multi
    def create_lines(self): 
    
       
        sequence = 0
        for line in self.cotizacion_id.line_ids:
            if line.sequence > sequence:
                sequence = line.sequence
        sequence = sequence + 1
    
        if self.referencia_cliente_id and self.attribute_id and len(self.oferta_ids)>0:
            for oferta in self.oferta_ids:
            
                cantonera_impresion_id = None
                if oferta.attribute_id.cantonera_impresion_id:
                    cantonera_impresion_id = oferta.attribute_id.cantonera_impresion_id.id
                    
                reciclable_id = None
                if oferta.attribute_id.reciclable_id:
                    reciclable_id = oferta.attribute_id.reciclable_id.id
            
            
                if len(self.env['sale.cotizacion.line'].search([('cotizacion_id', '=', self.cotizacion_id.id), ('oferta_id', '=', oferta.id)])) <= 0:   
                    sale = self.env['sale.cotizacion.line'].create({'cotizacion_id': self.cotizacion_id.id, 
                                                                    'referencia_cliente_id':self.referencia_cliente_id.id, 
                                                                    'attribute_id': self.attribute_id.id,
                                                                    'oferta_id': oferta.id,
                                                                    'npallets': oferta.num_pallets,
                                                                    'emetro': oferta.emetro,
                                                                    'eton': oferta.eton,
                                                                    'sequence': sequence,
                                                                    'cantonera_impresion_id': cantonera_impresion_id,
                                                                    'reciclable_id': reciclable_id,
                                                                    'und_pallet': oferta.und_pallet
                                                                  })
                    sequence = sequence + 1

        return {}
    
    
    
    
    
    
    