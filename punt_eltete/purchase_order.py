from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    lot_ids = fields.One2many('stock.production.lot', 'purchase_order_line_id', string="Lotes", )
    attribute_id = fields.Many2one('sale.product.attribute', string="Atributo producto", )
    oferta_id = fields.Many2one('sale.offer.oferta', string="Oferta")
    
    
    @api.multi
    def action_view_form_purchase_order(self):
        view = self.env.ref('purchase.purchase_order_line_form2')
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'purchase.order.line',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'res_id': self.id,
            'context': self.env.context,
        }
    
    
    
    
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def create_purchase_order_line_referencia(self, referencia_cliente_id, attribute_id, oferta_id, num_pallets):
        for record in self:
        


            product_id = None
            for prod in self.env['product.template'].search([('referencia_id', '=', referencia_cliente_id.referencia_id.id),
                                                             ]):
                product_id = prod
 
            if product_id == None:
                es_vendido = False
                es_comprado = False
                tipo_producto = ''
                cuenta_ingresos_code = -1
                cuenta_gastos_code = -1
                
                if referencia_cliente_id.is_cantonera == True:
                    es_vendido = True
                    es_comprado = False
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70100001
                    cuenta_gastos_code = -1
                if referencia_cliente_id.is_perfilu == True:
                    es_vendido = True
                    es_comprado = True
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000008
                    cuenta_gastos_code = 60000003
                if referencia_cliente_id.is_slipsheet == True:
                    es_vendido = True
                    es_comprado = False
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70100009
                    cuenta_gastos_code = -1
                if referencia_cliente_id.is_solidboard == True:
                    es_vendido = True
                    es_comprado = False
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000011
                    cuenta_gastos_code = -1
                if referencia_cliente_id.is_formato == True:
                    es_vendido = True
                    es_comprado = True
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000004
                    cuenta_gastos_code = 60000004
                if referencia_cliente_id.is_bobina == True:
                    es_vendido = True
                    es_comprado = True
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000004
                    cuenta_gastos_code = 60000004
                if referencia_cliente_id.is_pieballet == True:
                    es_vendido = True
                    es_comprado = True
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000002
                    cuenta_gastos_code = 60000005
                if referencia_cliente_id.is_flatboard == True:
                    es_vendido = True
                    es_comprado = True
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000005
                    cuenta_gastos_code = 60000007
                if referencia_cliente_id.is_varios == True:
                    es_vendido = True
                    es_comprado = True
                    tipo_producto = 'consu'
                    cuenta_gastos_code = -1
                    if referencia_cliente_id.tipo_varios_id:
                        cuenta_ingresos_code = referencia_cliente_id.tipo_varios_id.number
                if referencia_cliente_id.is_mprima_papel == True:
                    es_vendido = True
                    es_comprado = False
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000004
                    cuenta_gastos_code = 60100001
                
                product_id = self.env['product.template'].create({'name': referencia_cliente_id.referencia_id.name, 
                                                                  'type': tipo_producto,
                                                                  'purchase_ok': es_comprado,
                                                                  'sale_ok': es_vendido,
                                                                  'tracking': 'serial',
                                                                  'categ_id': referencia_cliente_id.type_id.id,
                                                                  'referencia_id':referencia_cliente_id.referencia_id.id, 
                                                                  #'property_account_income_id': 
                                                                  #'property_account_expense_id': 
                                                                 })
                
                
                
                
            purchase_line = self.env['purchase.order.line'].create({'order_id': record.id, 
                                                'name':product_id.name, 
                                                'product_uom_qty': num_pallets,
                                                'product_qty': num_pallets,
                                                'price_unit': 0.0,
                                                'date_planned': fields.Date.today(),
                                                'product_uom': 1,
                                                'attribute_id': attribute_id.id,
                                                'oferta_id': oferta_id.id,
                                                'product_id': product_id.product_variant_id.id,
                                               })
            purchase_line._compute_tax_id()
    
