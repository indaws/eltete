from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    attribute_id = fields.Many2one('sale.product.attribute', string="Atributo producto", )
    oferta_id = fields.Many2one('sale.offer.oferta', string="Oferta")

    lot_ids = fields.One2many('stock.production.lot', 'purchase_order_line_id', string="Lotes", )
    cliente_id = fields.Many2one('res.partner', string="Cliente")
    sale_line_id = fields.Many2one('sale.order.line', string="Línea Venta")
    
    und_pallet = fields.Integer('Und Pallet', readonly = True, compute = "_get_descripcion")
    peso_neto_pallet = fields.Integer('Peso Neto Pallet', readonly = True, compute = "_get_descripcion")
    descripcion_bemeco = fields.Html('Descricion Bemeco', readonly = True, compute = "_get_descripcion")
    descripcion_proveedor = fields.Html('Descricion Proveedor', readonly = True, compute = "_get_descripcion")
    comentario_proveedor = fields.Char('Comentario', readonly = True, compute = "_get_descripcion")
    tipo_unidad = fields.Char('Tipo', readonly = True, compute = "_get_descripcion")
    
    precio_num = fields.Float('Precio', digits = (12,4), related='sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.precio', readonly = False)
    num_pallets = fields.Integer('Num Pallets')
    kg_pedidos = fields.Float('Cantidad kg', digits = (12,4))
    importe_pedido = fields.Float('Importe Pedido', digits = (10, 2), readonly = True, compute = "_get_importe_pedido")
    cantidad_pedida = fields.Html('Cantidad Pedida', readonly = True, compute = "_get_importe_pedido")
    precio = fields.Html('Precio', readonly = True, compute = "_get_importe_pedido")
    
    importe_llegado = fields.Float('Importe LLegado', digits = (10, 2), readonly = True, compute = "_get_valores")
    peso_neto = fields.Integer('Peso Neto', readonly = True, compute = "_get_valores")
    unidades = fields.Integer('Unidades', readonly = True, compute = "_get_valores")
    num_lotes = fields.Integer('Num Lotes', readonly = True, compute = "_get_valores")
    
    #precio_ref = fields.Float('Precio Ref', related='sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.precio', readonly = False)
   
            
    @api.onchange('num_pallets')
    def _onchange_precio(self):
        if self.product_id.categ_id.is_formato == True:
            self.precio_num = 0.62
        if self.product_id.categ_id.is_bobina == True:
            self.precio_num = 0.56
    
    
    
    @api.onchange('precio_num', 'num_lotes', 'lot_ids', 'peso_neto', 'unidades')
    def _onchange_cantidades(self):
        if self.product_id.categ_id:
            if self.product_id.categ_id.is_mprima_cola == True or self.product_id.categ_id.is_mprima_papel == True:
                self.product_qty = self.peso_neto
                self.product_uom_qty = self.peso_neto
                self.price_unit = self.precio_num
                
            elif self.product_id.categ_id.is_formato == True or self.product_id.categ_id.is_bobina == True:
                self.product_qty = self.num_lotes
                self.product_uom_qty = self.num_lotes
                if self.num_lotes > 0:
                    self.price_unit = self.precio_num * self.peso_neto / self.num_lotes
                    
            else:
                self.product_qty = self.num_lotes
                self.product_uom_qty = self.num_lotes
                if self.num_lotes > 0:
                    self.price_unit = self.precio_num * self.unidades / self.num_lotes

    
    @api.depends('sale_line_id', 'product_id')
    def _get_descripcion(self):
        for record in self:
            descripcion_bemeco = ""
            descripcion_proveedor = ""
            comentario_proveedor = ""
            tipo_unidad = ""
            peso_neto_pallet = 0
            und_pallet = 0
            if record.sale_line_id:
                if record.sale_line_id.oferta_id:
                    und_pallet = record.sale_line_id.oferta_id.unidades
                    if record.sale_line_id.oferta_id.attribute_id.titulo:
                        descripcion_bemeco = record.sale_line_id.oferta_id.attribute_id.titulo
                    if record.sale_line_id.oferta_id.attribute_id.descripcion_proveedor:
                        descripcion_proveedor = record.sale_line_id.oferta_id.attribute_id.descripcion_proveedor
                    if record.sale_line_id.oferta_id.attribute_id.comentario_proveedor:
                        comentario_proveedor = record.sale_line_id.oferta_id.attribute_id.comentario_proveedor    
                    
                    peso_neto_pallet = record.sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro
                    peso_neto_pallet = peso_neto_pallet * record.sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
                    peso_neto_pallet = peso_neto_pallet * und_pallet
             
            if record.product_id.categ_id.is_mprima_papel == True or record.product_id.categ_id.is_mprima_cola == True:
                tipo_unidad = "Kilo"
            elif record.product_id.categ_id.is_formato == True or record.product_id.categ_id.is_bobina == True:
                tipo_unidad = "Kilo"
            else:
                tipo_unidad = "Unidad"
            
            record.und_pallet = und_pallet
            record.descripcion_bemeco = descripcion_bemeco
            record.descripcion_proveedor = descripcion_proveedor
            record.comentario_proveedor = comentario_proveedor
            record.tipo_unidad = tipo_unidad
            record.peso_neto_pallet = peso_neto_pallet

    
    @api.depends('product_id', 'num_pallets', 'kg_pedidos', 'precio_num', 'und_pallet', 'peso_neto_pallet')
    def _get_importe_pedido(self):
        for record in self:
            importe = 0
            cantidad = ""
            cantidad_num = 0
            precio = ""
            if record.product_id:
                if record.product_id.categ_id.is_mprima_cola == True or record.product_id.categ_id.is_mprima_papel == True:
                    cantidad_num = record.kg_pedidos
                    importe = cantidad_num * record.precio_num
                    cantidad = str(cantidad_num) + "<br/>" + "Kg"
                    precio = str(record.precio_num) + "<br/>" + "€/kg"
                elif record.product_id.categ_id.is_formato == True or record.product_id.categ_id.is_bobina == True:
                    cantidad_num = record.peso_neto_pallet * record.num_pallets
                    importe = cantidad_num * record.precio_num
                    cantidad = str(cantidad_num) + "<br/>" + "Kg"
                    precio = str(record.precio_num) + "<br/>" + "€/kg"
                else:
                    cantidad_num = record.und_pallet * record.num_pallets
                    importe = record.und_pallet * record.num_pallets * record.precio_num
                    cantidad = str(cantidad_num) + "<br/>" + "Unidades"
                    precio = str(record.precio_num) + "<br/>" + "€/unidad"
                    
            record.importe_pedido = importe
            record.cantidad_pedida = cantidad
            record.precio = precio
    
    
    
    @api.depends('lot_ids', 'precio')
    def _get_valores(self):
        for record in self:
            unidades = 0
            peso_neto = 0
            importe = 0
            for lot in record.lot_ids:
                unidades = unidades + lot.unidades
                peso_neto = peso_neto + lot.peso_neto
                
            if record.product_id.categ_id.is_mprima_cola == True or record.product_id.categ_id.is_mprima_papel == True:
                importe = record.precio_num * peso_neto
            elif record.product_id.categ_id.is_formato == True or record.product_id.categ_id.is_bobina == True:
                importe = record.precio_num * peso_neto
            else:
                importe = record.precio_num * unidades
             
            record.num_lotes = len(record.lot_ids)
            record.peso_neto = peso_neto
            record.unidades = unidades
            record.importe_llegado = importe
                 
    
    
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
    importe_pedido = fields.Float('Importe Pedido', digits = (10, 2), readonly = True, compute = "_get_importe")
    importe_llegado = fields.Float('Importe Llegado', digits = (10, 2), readonly = True, compute = "_get_importe")
    iva_pedido = fields.Float('IVA Pedido', digits = (10, 2), readonly = True, compute = "_get_importe")
    iva_llegado = fields.Float('IVA Llegado', digits = (10, 2), readonly = True, compute = "_get_importe")
    total_pedido = fields.Float('Total Pedido', digits = (10, 2), readonly = True, compute = "_get_total")
    total_llegado = fields.Float('Total Llegado', digits = (10, 2), readonly = True, compute = "_get_total")
    
    
    @api.depends('importe_pedido', 'importe_llegado', 'iva_pedido', 'iva_llegado')
    def _get_total(self):
        for record in self:
            total_pedido = importe_pedido
            total_llegado = importe_llegado
            
            record.total_pedido = total_pedido
            record.total_llegado = total_llegado
    
    
    
    @api.depends('order_line', 'partner_id')
    def _get_importe(self):
        for record in self:
            importe_pedido = 0
            importe_llegado = 0
            iva_pedido = 0
            iva_llegado = 0
            
            for linea in self.order_line:
                importe_pedido = importe_pedido + linea.importe_pedido
                importe_llegado = importe_llegado + linea.importe_llegado
                
            if record.partner_id.property_account_position_id.id == 1:
                iva_pedido = importe_pedido * 0.21
                iva_llegado = importe_llegado * 0.21
            
            record.importe_pedido = importe_pedido
            record.importe_llegado = importe_llegado
            record.iva_pedido = iva_pedido
            record.iva_llegado = iva_llegado

            
    @api.multi
    def create_purchase_order_line_referencia(self, cliente_id, sale_line_id, num_pallets):
        for record in self:
        
        
            referencia_cliente_id = sale_line_id.attribute_id.referencia_cliente_id
            attribute_id = sale_line_id.attribute_id
            oferta_id = sale_line_id.oferta_id
        
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
                medida = product_id.uom_id.id
                
                
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
                                                'sale_line_id': sale_line_id.id,
                                               })
            purchase_line._compute_tax_id()
    
