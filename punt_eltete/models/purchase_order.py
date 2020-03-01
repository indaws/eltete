from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    lot_ids = fields.One2many('stock.production.lot', 'purchase_order_line_id', string="Lotes", )
    attribute_id = fields.Many2one('sale.product.attribute', string="Atributo producto", )
    oferta_id = fields.Many2one('sale.offer.oferta', string="Oferta")
    cliente_id = fields.Many2one('res.partner', string="Cliente")
    
    descripcion_bemeco = fields.Char('Descricion Bemeco', readonly = True, compute = "_get_descripcion")
    descripcion_proveedor = fields.Html('Descricion Proveedor', readonly = True, compute = "_get_descripcion")
    comentario_proveedor = fields.Char('Comentario_proveedor', readonly = True, compute = "_get_descripcion")
    
    precio_kilo = fields.Float('Precio kg', digits = (12,4))
    precio_und = fields.Float('Precio Ud', digits = (12,4))
    num_pallets = fields.Integer('Num Pallets')
    importe = fields.Float('Importe', digits = (10, 2), readonly = True, compute = "_get_importe")
    
    peso_neto = fields.Integer('Peso Neto', readonly = True, compute = "_get_valores")
    unidades = fields.Integer('Unidades', readonly = True, compute = "_get_valores")
    num_lotes = fields.Integer('Num Lotes', readonly = True, compute = "_get_valores")
    
    @api.depends('oferta_id')
    def _get_descripcion(self):
        for record in self:
            descripcion_bemeco = ""
            descripcion_proveedor = ""
            comentario_proveedor = ""
            if record.oferta_id:
                if record.oferta_id.attribute_id.titulo:
                    descripcion_bemeco = record.oferta_id.attribute_id.titulo
                if record.oferta_id.attribute_id.titulo:
                    descripcion_proveedor = record.oferta_id.attribute_id.descripcion_proveedor
                if record.oferta_id.attribute_id.comentario_proveedor:
                    comentario_proveedor = record.oferta_id.attribute_id.comentario_proveedor
            
            record.descripcion_bemeco = descripcion_bemeco
            record.descripcion_proveedor = descripcion_proveedor
            record.comentario_proveedor = comentario_proveedor
                
    
    @api.onchange('num_pallets')
    def _onchange_precio(self):
        if self.product_id.categ_id.is_formato == True:
            self.precio_kilo = 0.62
        if self.product_id.categ_id.is_bobina == True:
            self.precio_kilo = 0.56
    
    
    
    @api.onchange('precio_kilo', 'precio_und', 'num_lotes', 'lot_ids', 'lot_ids.peso_neto', 'lot_ids.unidades')
    def _onchange_cantidades(self):
        if self.product_id.categ_id:
            if self.product_id.categ_id.is_mprima_cola == True or self.product_id.categ_id.is_mprima_papel == True:
                self.product_qty = self.peso_neto
                self.product_uom_qty = self.peso_neto
                self.price_unit = self.precio_kilo
                
            elif self.product_id.categ_id.is_formato == True or self.product_id.categ_id.is_bobina == True:
                self.product_qty = self.num_pallets
                self.product_uom_qty = self.num_pallets
                if self.num_lotes > 0:
                    self.price_unit = self.precio_kilo * self.peso_neto / self.num_lotes
            else:
                self.product_qty = self.num_pallets
                self.product_uom_qty = self.num_pallets
                if self.num_lotes > 0:
                    self.price_unit = self.precio_und * self.unidades / self.num_lotes
    
    
    @api.depends('product_id', 'oferta_id', 'num_pallets', 'precio_kilo', 'precio_und')
    def _get_importe(self):
        for record in self:
            cantidad = 0
            precio = 0
            importe = 0
            if record.oferta_id:
                if record.product_id.categ_id.is_mprima_cola == True or record.product_id.categ_id.is_mprima_papel == True:
                    x = 0
                elif record.product_id.categ_id.is_formato == True or record.product_id.categ_id.is_bobina == True:
                    precio = record.precio_kilo
                    cantidad = record.num_pallets * record.oferta_id.peso_neto
                else:
                    precio = record.precio_und
                    cantidad = record.num_pallets * record.oferta_id.und_pallet
                    
                importe = precio * cantidad

            record.importe = importe          
    
    
    
    @api.depends('lot_ids')
    def _get_valores(self):
        for record in self:
        
            record.num_lotes = len(record.lot_ids)
            unidades = 0
            peso_neto = 0
            for lot in record.lot_ids:
                unidades = unidades + lot.unidades
                peso_neto = peso_neto + lot.peso_neto
                
            record.peso_neto = peso_neto
            record.unidades = unidades
                 
    
    
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
    def create_purchase_order_line_referencia(self, cliente_id, referencia_cliente_id, attribute_id, oferta_id, num_pallets):
        for record in self:
        
            medida = -1

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
                    medida = 1
                    cuenta_ingresos_code = 70100001
                    cuenta_gastos_code = -1
                if referencia_cliente_id.is_perfilu == True:
                    es_vendido = True
                    es_comprado = True
                    medida = 1
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000008
                    cuenta_gastos_code = 60000003
                if referencia_cliente_id.is_slipsheet == True:
                    es_vendido = True
                    es_comprado = False
                    medida = 1
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70100009
                    cuenta_gastos_code = -1
                if referencia_cliente_id.is_solidboard == True:
                    es_vendido = True
                    es_comprado = False
                    medida = 1
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000011
                    cuenta_gastos_code = -1
                if referencia_cliente_id.is_formato == True:
                    es_vendido = True
                    es_comprado = True
                    medida = 1
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000004
                    cuenta_gastos_code = 60000004
                if referencia_cliente_id.is_bobina == True:
                    es_vendido = True
                    es_comprado = True
                    medida = 1
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000004
                    cuenta_gastos_code = 60000004
                if referencia_cliente_id.is_pieballet == True:
                    es_vendido = True
                    es_comprado = True
                    medida = 1
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000002
                    cuenta_gastos_code = 60000005
                if referencia_cliente_id.is_flatboard == True:
                    es_vendido = True
                    es_comprado = True
                    medida = 1
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000005
                    cuenta_gastos_code = 60000007
                if referencia_cliente_id.is_varios == True:
                    es_vendido = True
                    es_comprado = True
                    medida = 1
                    tipo_producto = 'consu'
                    cuenta_gastos_code = -1
                    if referencia_cliente_id.tipo_varios_id:
                        cuenta_ingresos_code = referencia_cliente_id.tipo_varios_id.number
                if referencia_cliente_id.is_mprima_papel == True:
                    es_vendido = True
                    es_comprado = False
                    medida = 3 // kg
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
                
            else:
                medida = product_id.uom_id
                
                
            purchase_line = self.env['purchase.order.line'].create({'order_id': record.id, 
                                                'name':product_id.name, 
                                                'product_uom_qty': 0.0,
                                                'product_qty': 0.0,
                                                'price_unit': 0.0,
                                                'date_planned': fields.Date.today(),
                                                'product_uom': medida,
                                                'cliente_id': cliente_id.id,
                                                'attribute_id': attribute_id.id,
                                                'oferta_id': oferta_id.id,
                                                'product_id': product_id.product_variant_id.id,
                                               })
            purchase_line._compute_tax_id()
    
