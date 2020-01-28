from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)



class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    
    num_pallets = fields.Integer('Num pallets', readonly = True, compute = "_get_num_pallets")
    
    @api.depends('invoice_line_ids', 'invoice_line_ids.quantity')
    def _get_num_pallets(self):
        for record in self:
            num_pallets = 0
            for line in record.invoice_line_ids:
                if line.product_id:
                    if line.product_id.type == 'product':
                        num_pallets = num_pallets + line.quantity
            record.num_pallets = num_pallets
    
    
    pedido_cliente = fields.Char('Pedido cliente', compute = "_get_datos_lineas")
    fecha_entrega_albaran = fields.Date('Fecha albarán', compute = "_get_datos_lineas")
    
    @api.depends('invoice_line_ids')
    def _get_datos_lineas(self):
        for record in self:
            num_pallets = 0
            for line in record.invoice_line_ids:
                pedido_cliente = line.pedido_cliente
                fecha_entrega_albaran = line.fecha_albaran
            record.pedido_cliente = pedido_cliente
            record.fecha_entrega_albaran = fecha_entrega_albaran
            
            
    importe_sin_descuento = fields.Float('Importe Sin Descuento', digits = (10, 2), compute="_get_valores_descuento")
    descuento_porcentaje = fields.Float('Descuento Cliente', digits = (10, 2), readonly = True, compute="_get_valores_descuento")
    
    
    @api.depends('invoice_line_ids')
    def _get_valores_descuento(self):
    
        for record in self:

            importe_sin_descuento = 0
            descuento_porcentaje = 0.0
            
            for line in record.invoice_line_ids:
                importe_sin_descuento = importe_sin_descuento + line.importe
                if line.discount > 0.0:
                    descuento_porcentaje = line.discount

            record.descuento_porcentaje = descuento_porcentaje
            record.importe_sin_descuento = importe_sin_descuento





class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    
    #Campos calculados
    codigo_cliente = fields.Char('Código cliente', readonly = True, compute = "_get_valores")
    descripcion = fields.Html('Descripción', readonly = True, compute = "_get_valores")
    und_pallet = fields.Integer('Unidades Pallet', readonly = True, compute = "_get_valores")
    cantidad = fields.Char('Cantidad', compute = "_get_valores")
    precio = fields.Char('Precio', readonly = True, compute = "_get_valores")
    importe = fields.Float('Importe', digits = (10,2), readonly = True, compute = "_get_valores")
    peso_neto = fields.Integer('Peso Neto Pallet', readonly = True, compute = "_get_valores")
    peso_bruto = fields.Integer('Peso Bruto Pallet', readonly = True, compute = "_get_valores")
    eton = fields.Float('Eton', digits=(8, 1), readonly = True, compute = "_get_valores")
    
    
    num_albaran = fields.Char('Num albarán', compute = "_get_datos_albaran")
    fecha_albaran = fields.Date('Fecha albarán', compute = "_get_datos_albaran")
    
    pedido_cliente = fields.Char('Pedido cliente', compute = "_get_datos_pedido")
    
    
    
    
    @api.depends('move_line_ids')
    def _get_datos_albaran(self):
        for record in self:
            num_albaran = ''
            fecha_albaran = ''
            for move in record.move_line_ids:
                num_albaran = move.picking_id.name
                fecha_albaran = move.picking_id.scheduled_date.date()
            record.num_albaran = num_albaran
            record.fecha_albaran = fecha_albaran
            
            
    @api.depends('sale_line_ids')
    def _get_datos_pedido(self):
        for record in self:
            pedido_cliente = ''
            for sale in record.sale_line_ids:
                pedido_cliente = sale.order_id.pedido_cliente
            record.pedido_cliente = pedido_cliente
                
    
    
    @api.depends('sale_line_ids')
    def _get_valores(self):
        for record in self:
        
            sale_line_id = None
            for sale in record.sale_line_ids:
                sale_line_id = sale
        
        
            if sale_line_id:
        
                codigo_cliente = sale_line_id.oferta_id.attribute_id.codigo_cliente
                descripcion = ''
                if sale_line_id.oferta_id:
                    descripcion = sale_line_id.oferta_id.attribute_id.titulo
                und_pallet = 0
                cantidad = ""
                precio = ""
                importe = 0
                peso_neto = 0
                peso_bruto = 0
                eton = 0

                if sale_line_id.und_user > 0:
                    und_pallet = sale_line_id.und_user
                else:
                    und_pallet = sale_line_id.oferta_id.unidades
                
                facturar = sale_line_id.oferta_id.attribute_id.referencia_cliente_id.precio_cliente
                cantidad_num = 0
                precio_num = 0
                #metros
                if facturar == '1':
                    cantidad_num = record.quantity * und_pallet * sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
                    cantidad_num = round(cantidad_num, 4)
                    cantidad = str(cantidad_num) + " metros"
                    precio_num = sale_line_id.oferta_id.precio_metro
                    precio_num = round(precio_num, 4)
                    precio = str(precio_num) + " €/metro"
                    if sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro > 0:
                        eton = sale_line_id.oferta_id.precio_metro * 1000 / sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro
                    
                    if sale_line_id.kilos_user > 0:
                        peso_bruto = sale_line_id.kilos_user
                        peso_neto = peso_bruto - 15
                    else:
                        peso_neto = sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro * sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
                        peso_neto = peso_neto * und_pallet
                    
                        pesoMadera = 0
                        if sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud < 1500:
                            pesoMadera = 15
                        elif sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud < 2000:
                            pesoMadera = 20
                        else:
                            pesoMadera = int(sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud / 1000) * 15
                        peso_bruto = int((peso_neto + pesoMadera) / 5) * 5
                #unidades
                elif facturar == '2':
                    cantidad_num = record.quantity * und_pallet
                    cantidad_num = round(cantidad_num, 4)
                    cantidad = str(cantidad_num) + " unidades"
                    precio_num = sale_line_id.oferta_id.precio_metro * sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
                    precio_num = round(precio_num, 4)
                    precio = str(precio_num) + " €/unidad"
                    if sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro > 0:
                        eton = sale_line_id.oferta_id.precio_metro * 1000 / sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro
                    
                    if sale_line_id.kilos_user > 0:
                        peso_bruto = sale_line_id.kilos_user
                        peso_neto = peso_bruto - 15
                    else:
                        peso_neto = sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro * sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
                        peso_neto = peso_neto * und_pallet
                    
                        pesoMadera = 0
                        if sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud < 1500:
                            pesoMadera = 15
                        elif sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud < 2000:
                            pesoMadera = 20
                        else:
                            pesoMadera = int(sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud / 1000) * 15
                        peso_bruto = int((peso_neto + pesoMadera) / 5) * 5
                #Millares
                elif facturar == '3':
                    cantidad_num = record.quantity * und_pallet / 1000
                    cantidad_num = round(cantidad_num, 4)
                    cantidad = str(cantidad_num) + " millares"
                    precio_num = sale_line_id.oferta_id.precio_metro * sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad * 1000
                    precio_num = round(precio_num, 4)
                    precio = str(precio_num) + " €/millar"
                    if sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro > 0:
                        eton = sale_line_id.oferta_id.precio_metro * 1000 / sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro
                    
                    if sale_line_id.kilos_user > 0:
                        peso_bruto = sale_line_id.kilos_user
                        peso_neto = peso_bruto - 15
                    else:
                        peso_neto = sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro * sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
                        peso_neto = peso_neto * und_pallet
                    
                        pesoMadera = 0
                        if sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud < 1500:
                            pesoMadera = 15
                        elif sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud < 2000:
                            pesoMadera = 20
                        else:
                            pesoMadera = int(sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud / 1000) * 15
                        peso_bruto = int((peso_neto + pesoMadera) / 5) * 5
                #Kilos
                elif facturar == '4':
                    if sale_line_id.kilos_user > 0:
                        peso_neto = sale_line_id.kilos_user - 15
                        peso_bruto = sale_line_id.kilos_user
                    else:
                        peso_neto = sale_line_id.oferta_id.kilos
                        peso_bruto = peso_neto + 15
                    cantidad_num = record.quantity * peso_neto
                    cantidad_num = round(cantidad_num, 4)
                    cantidad = str(cantidad_num) + " kilos"
                    precio_num = sale_line_id.oferta_id.precio_kilo
                    precio_num = round(precio_num, 4)
                    precio = str(precio_num) + " €/kilo"
                    eton = sale_line_id.oferta_id.precio_kilo * 1000
                #Varios
                elif facturar == '5':
                    cantidad_num = record.quantity * und_pallet
                    cantidad_num = round(cantidad_num, 4)
                    cantidad = str(cantidad_num) + " unidades"
                    precio_num = sale_line_id.oferta_id.precio_varios
                    precio_num = round(precio_num, 4)
                    precio = str(precio_num) + " €/unidad"
                    peso_neto = 0
                    peso_bruto = 0
                
                importe = precio_num * cantidad_num
                
                record.codigo_cliente = codigo_cliente
                record.descripcion = descripcion
                record.und_pallet = und_pallet
                record.cantidad = cantidad
                record.precio = precio
                record.importe = importe
                record.peso_neto = peso_neto
                record.peso_bruto = peso_bruto
                record.eton = eton
            
            