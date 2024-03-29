from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)
from odoo import exceptions
import requests



class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    num_pallets = fields.Integer('Num pallets', readonly = True, compute = "_get_num_pallets")
    peso_neto = fields.Integer('Peso Neto', readonly = True, compute = "_get_num_pallets")
    peso_bruto = fields.Integer('Peso Bruto', readonly = True, compute = "_get_num_pallets")
    peso_neto_mojado = fields.Integer('Peso Neto Mojado', readonly = True, compute = "_get_num_pallets")
    peso_bruto_mojado = fields.Integer('Peso Bruto Mojado', readonly = True, compute = "_get_num_pallets")
    neto_mojado_user = fields.Integer('Neto User')
    bruto_mojado_user = fields.Integer('Bruto User')
    
    importe_cantonera = fields.Float('Importe Cantonera', digits = (10, 2), readonly = True, compute = "_get_num_pallets")
    peso_cantonera = fields.Integer('Peso Cantonera', readonly = True, compute = "_get_num_pallets")
    eton_cantonera = fields.Integer('Eton Cantonera', readonly = True, compute = "_get_num_pallets")
    importe_perfilu = fields.Float('Importe Perfil U', digits = (10, 2), readonly = True, compute = "_get_num_pallets")
    peso_perfilu = fields.Integer('Peso Perfil U', readonly = True, compute = "_get_num_pallets")
    eton_perfilu = fields.Integer('Eton Perfil U', readonly = True, compute = "_get_num_pallets")
    importe_slipsheet = fields.Float('Importe Slip Sheet', digits = (10, 2), readonly = True, compute = "_get_num_pallets")
    peso_slipsheet = fields.Integer('Peso Slip Sheets', readonly = True, compute = "_get_num_pallets")
    eton_slipsheet = fields.Integer('Eton Slip Sheets', readonly = True, compute = "_get_num_pallets")
    importe_formato = fields.Float('Importe Formato', digits = (10, 2), readonly = True, compute = "_get_num_pallets")
    peso_formato = fields.Integer('Peso Formato', readonly = True, compute = "_get_num_pallets")
    eton_formato = fields.Integer('Eton Formato', readonly = True, compute = "_get_num_pallets")
    importe_bobina = fields.Float('Importe Bobina', digits = (10, 2), readonly = True, compute = "_get_num_pallets")
    peso_bobina = fields.Integer('Peso Bobina', readonly = True, compute = "_get_num_pallets")
    eton_bobina = fields.Integer('Eton Bobina', readonly = True, compute = "_get_num_pallets")
    importe_solidboard = fields.Float('Importe Solid Board', digits = (10, 2), readonly = True, compute = "_get_num_pallets")
    peso_solidboard = fields.Integer('Peso Solid Board', readonly = True, compute = "_get_num_pallets")
    eton_solidboard = fields.Integer('Eton Solid Board', readonly = True, compute = "_get_num_pallets")
    importe_pie = fields.Float('Importe Pie Pallet', digits = (10, 2), readonly = True, compute = "_get_num_pallets")
    peso_pie = fields.Integer('Peso Pie Pallet', readonly = True, compute = "_get_num_pallets")
    eton_pie = fields.Integer('Eton Pie Pallet', readonly = True, compute = "_get_num_pallets")
    importe_flatboard = fields.Float('Importe Flat Board', digits = (10, 2), readonly = True, compute = "_get_num_pallets")
    peso_flatboard = fields.Integer('Peso Flat Board', readonly = True, compute = "_get_num_pallets")
    eton_flatboard = fields.Integer('Eton Flat Board', readonly = True, compute = "_get_num_pallets")
    importe_varios = fields.Integer('Importe Varios', readonly = True, compute = "_get_num_pallets")
    
    importe_sin_descuento = fields.Float('Importe Sin Descuento', digits = (10, 2), compute="_get_valores_descuento")
    importe_descuento = fields.Float('Importe Dto PP', digits = (10, 2), compute="_get_valores_descuento")
    descuento_porcentaje = fields.Float('Descuento Cliente', digits = (10, 2), readonly = True, compute="_get_valores_descuento")
    
    pedido_cliente = fields.Char('Pedido cliente', compute = "_get_datos_lineas")
    fecha_entrega_albaran = fields.Date('Fecha albarán', compute = "_get_datos_lineas")
    numero_contenedor = fields.Char('Numero Contenedor', compute = "_get_datos_lineas")
    precinto_contenedor = fields.Char('Precinto Contenedor', compute = "_get_datos_lineas")
    carrier_id = fields.Many2one('delivery.carrier', string="Método Entrega", readonly = True, compute = "_get_datos_lineas")
    comercial_bueno_id = fields.Many2one('res.users', string='Comercial Bueno', compute="_get_comercial")
    
    actualizar = fields.Boolean('Comprobada')
    fsc_venta = fields.Boolean('FSC Venta', default = False)
    fsc_enlaces = fields.Html('FSC Enlaces')
    
    vendido = fields.Char('DATA', readonly = True, compute = '_get_vendido') 

    #Proveedor
    importe_ajustado = fields.Float('Importe a ajustar', digits = (10, 2))
    
    @api.multi
    def ajustar_importe_factura(self):
        for record in self:
            if record.state == 'draft' and record.type == 'in_invoice' and record.importe_ajustado > 0.0:
                diferencia = record.amount_untaxed - record.importe_ajustado
                
                if diferencia != 0.0:
                    for line in record.invoice_line_ids:
                        importe_a_sumar = diferencia / line.quantity
                        line.price_unit = line.price_unit - importe_a_sumar
                        
                        if record.amount_untaxed == record.importe_ajustado:
                            break
                        diferencia = record.amount_untaxed - record.importe_ajustado
    
    
    @api.model
    def create(self, values):
        res = super(AccountInvoice, self).create(values)
        for invoice in res:
            if invoice.type == 'out_invoice':
                for line in invoice.invoice_line_ids:
                    precio_unidad = 0
                    num_pallets = 0
                    if line.num_pallets > 0:
                        precio_unidad = line.importe / line.num_pallets
                        num_pallets = line.num_pallets
                    elif line.facturar == '5':
                        precio_unidad = line.importe
                        num_pallets = 1
                    line.price_unit = precio_unidad
                    line.quantity = num_pallets
        # here you can do accordingly
        return res
    
    
    @api.onchange('actualizar')
    def _onchange_actualizar(self):
        for record in self:  
            fsc_venta = False
            fsc_enlaces = ""
            
            for line in record.invoice_line_ids:
                precio_unidad = 0
                num_pallets = 0
                if line.num_pallets > 0:
                    precio_unidad = line.importe / line.num_pallets
                    num_pallets = line.num_pallets
                elif line.facturar == '5':
                    precio_unidad = line.importe
                    num_pallets = 1
                line.price_unit = precio_unidad
                line.quantity = num_pallets
                
                if line.fsc_venta == True:
                    fsc_venta = True
                    
                    #Buscamos sus pallets
                    venta_id = None
                    for sale in line.sale_line_ids:
                        venta_id = sale
                        if venta_id:
                            for lote in venta_id.lot_ids:
                                enlace = "http://bemecopack.es/jseb/ventafsc_vender.php?pallet=" + lote.name + "&fecha=" + str(record.date_invoice)
                                fsc_enlaces = fsc_enlaces + enlace + "<br/>"
                            
            record.fsc_venta = fsc_venta
            record.fsc_enlaces = fsc_enlaces

            
            
    @api.depends('invoice_line_ids')
    def _get_vendido(self):
        for record in self:
            vendido = "OK"
            direccion = "http://bemecopack.es/jseb/ventaodoo.php?"
            
            for line in record.invoice_line_ids:
                if line.vendido != "":
                    enviar = direccion + line.vendido + "&fecha=" + str(record.date_invoice) + "&linea=" + str(record.id)
                    try:
                        respuesta1 = requests.get(enviar)
                        respuesta = respuesta1.text
                        
                        if respuesta != "OK":
                            vendido = "NO"
                    except:
                        vendido = "NO"
       
            record.vendido = vendido            
            
            
    
    @api.depends('partner_id')
    def _get_comercial(self):
        for record in self:
            record.comercial_bueno_id = record.partner_id.user_id.id
    
    
    
    @api.depends('invoice_line_ids', 'invoice_line_ids.quantity', 'neto_mojado_user', 'bruto_mojado_user')
    def _get_num_pallets(self):
        for record in self:
            num_pallets = 0
            peso_neto = 0
            peso_bruto = 0
            
            peso_neto_mojado = 0
            peso_bruto_mojado = 0
            
            peso_cantonera = 0
            importe_cantonera = 0
            eton_cantonera = 0
            peso_perfilu = 0
            importe_perfilu = 0
            eton_perfilu = 0
            peso_slipsheet = 0
            importe_slipsheet = 0
            eton_slipsheet = 0
            peso_formato = 0
            importe_formato = 0
            eton_formato = 0
            peso_bobina = 0
            importe_bobina = 0
            eton_bobina = 0
            peso_solidboard = 0
            importe_solidboard = 0
            eton_solidboard = 0
            peso_pie = 0
            importe_pie = 0
            eton_pie = 0
            peso_flatboard = 0
            importe_flatboard = 0
            eton_flatboard = 0
            importe_varios = 0

            for line in record.invoice_line_ids:                
                if line.product_id:
                    if line.product_id.type == 'product':
                        num_pallets = num_pallets + line.num_pallets
                    
                if line.product_id.referencia_id.is_cantonera == True:
                    peso_cantonera = peso_cantonera + int(line.peso_neto)
                    importe_cantonera = importe_cantonera + line.price_subtotal
                if line.product_id.referencia_id.is_perfilu == True:
                    peso_perfilu = peso_perfilu + int(line.peso_neto)
                    importe_perfilu = importe_perfilu + line.price_subtotal
                if line.product_id.referencia_id.is_slipsheet == True:
                    peso_slipsheet = peso_slipsheet + int(line.peso_neto)
                    importe_slipsheet = importe_slipsheet + line.price_subtotal
                if line.product_id.referencia_id.is_formato == True:
                    peso_formato = peso_formato + int(line.peso_neto)
                    importe_formato = importe_formato + line.price_subtotal
                if line.product_id.referencia_id.is_bobina == True:
                    peso_bobina = peso_bobina + int(line.peso_neto)
                    importe_bobina = importe_bobina + line.price_subtotal
                if line.product_id.referencia_id.is_solidboard == True:
                    peso_solidboard = peso_solidboard + int(line.peso_neto)
                    importe_solidboard = importe_solidboard + line.price_subtotal
                if line.product_id.referencia_id.is_pieballet == True:
                    peso_pie = peso_pie + int(line.peso_neto)
                    importe_pie = importe_pie + line.price_subtotal
                if line.product_id.referencia_id.is_flatboard == True:
                    peso_flatboard = peso_flatboard + int(line.peso_neto)
                    importe_flatboard = importe_flatboard + line.price_subtotal
                if line.product_id.referencia_id.is_varios == True:
                    importe_varios = importe_varios + line.price_subtotal

                peso_neto = peso_neto + line.peso_neto
                peso_bruto = peso_bruto + line.peso_bruto
                peso_neto_mojado = peso_neto_mojado + line.peso_neto_mojado
                bruto_mojado = int(line.peso_bruto * 1.05 / 10) * 10
                peso_bruto_mojado = peso_bruto_mojado + bruto_mojado
                
            if peso_cantonera > 0:
                eton_cantonera = int(1000 * importe_cantonera / peso_cantonera)
            if peso_perfilu > 0:
                eton_perfilu = int(1000 * importe_perfilu / peso_perfilu)
            if peso_slipsheet > 0:
                eton_slipsheet = int(1000 * importe_slipsheet / peso_slipsheet)
            if peso_formato > 0:
                eton_formato = int(1000 * importe_formato / peso_formato)
            if peso_bobina > 0:
                eton_bobina = int(1000 * importe_bobina / peso_bobina)
            if peso_solidboard > 0:
                eton_solidboard = int(1000 * importe_solidboard / peso_solidboard)
            if peso_pie > 0:
                eton_pie = int(1000 * importe_pie / peso_pie)
            if peso_flatboard > 0:
                eton_flatboard = int(1000 * importe_flatboard / peso_flatboard)

            """
            divisor = 150000
            peso_neto_mojado = (1 + (peso_neto / divisor)) * peso_neto
            peso_neto_mojado = int(peso_neto_mojado / 5) * 5
            peso_bruto_mojado = (1 + (peso_bruto / divisor)) * peso_bruto
            peso_bruto_mojado = int(peso_bruto_mojado / 5) * 5
            
            if peso_bruto < 24000:
                while peso_bruto_mojado > 24000:
                    divisor = divisor + 10000
                    peso_neto_mojado = (1 + (peso_neto / divisor)) * peso_neto
                    peso_neto_mojado = int(peso_neto_mojado / 5) * 5
                    peso_bruto_mojado = (1 + (peso_bruto / divisor)) * peso_bruto
                    peso_bruto_mojado = int(peso_bruto_mojado / 5) * 5
                    
                if peso_neto_mojado < peso_neto:
                    peso_neto_mojado = peso_neto
                if peso_bruto_mojado < peso_bruto:
                    peso_bruto_mojado = peso_bruto 
            else:
                peso_neto_mojado = peso_neto
                peso_bruto_mojado = peso_bruto
            """
            
            if record.neto_mojado_user > 0:
                peso_neto_mojado = record.neto_mojado_user
            if record.bruto_mojado_user > 0:
                peso_bruto_mojado = record.bruto_mojado_user
             
            
            record.importe_cantonera = importe_cantonera
            record.peso_cantonera = peso_cantonera
            record.eton_cantonera = eton_cantonera
            record.importe_perfilu = importe_perfilu
            record.peso_perfilu = peso_perfilu
            record.eton_perfilu = eton_perfilu
            record.importe_slipsheet = importe_slipsheet
            record.peso_slipsheet = peso_slipsheet
            record.eton_slipsheet = eton_slipsheet
            record.importe_formato = importe_formato
            record.peso_formato = peso_formato
            record.eton_formato = eton_formato
            record.importe_bobina = importe_bobina
            record.peso_bobina = peso_bobina
            record.eton_bobina = eton_bobina
            record.importe_solidboard = importe_solidboard
            record.peso_solidboard = peso_solidboard
            record.eton_solidboard = eton_solidboard
            record.importe_pie = importe_pie
            record.peso_pie = peso_pie
            record.eton_pie = eton_pie
            record.importe_flatboard = importe_flatboard
            record.peso_flatboard = peso_flatboard
            record.eton_flatboard = eton_flatboard
            record.importe_varios = importe_varios

            record.num_pallets = num_pallets
            record.peso_neto = peso_neto
            record.peso_bruto = peso_bruto
            record.peso_neto_mojado = peso_neto_mojado
            record.peso_bruto_mojado = peso_bruto_mojado

            
    
    @api.depends('invoice_line_ids')
    def _get_datos_lineas(self):
        for record in self:
            num_pallets = 0
            pedido_cliente = ""
            carrier_id = None
            numero_contenedor = ""
            precinto_contenedor = ""
            fecha_entrega_albaran = None
            for line in record.invoice_line_ids:
                pedido_cliente = line.pedido_cliente
                fecha_entrega_albaran = line.fecha_albaran
                carrier_id = line.carrier_id.id
                numero_contenedor = line.numero_contenedor
                precinto_contenedor = line.precinto_contenedor
            record.pedido_cliente = pedido_cliente
            record.fecha_entrega_albaran = fecha_entrega_albaran
            record.carrier_id = carrier_id
            record.numero_contenedor = numero_contenedor
            record.precinto_contenedor = precinto_contenedor

            
            
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
            record.importe_descuento = record.amount_untaxed - record.importe_sin_descuento





class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    
    #Campos calculados
    codigo_cliente = fields.Char('Código cliente', readonly = True, compute = "_get_valores")
    descripcion = fields.Html('Descripción', readonly = True, compute = "_get_valores")
    precio_num = fields.Float('Precio', digits = (12, 4), readonly = True, compute = "_get_valores")
    precio = fields.Char('Precio', readonly = True, compute = "_get_valores")
    facturar = fields.Char('Facturar', readonly = True, compute = "_get_valores")
    cantidad_5_num = fields.Float('Cantidad 5', digits = (12, 4), readonly = True, compute = "_get_valores")
    
    num_albaran = fields.Char('Num albarán', compute = "_get_datos_albaran")
    fecha_albaran = fields.Date('Fecha albarán', compute = "_get_datos_albaran")
    cantidad_1_num = fields.Float('Cantidad 1', digits = (12, 4), readonly = True, compute = "_get_datos_albaran")
    cantidad_2_num = fields.Float('Cantidad 2', digits = (12, 4), readonly = True, compute = "_get_datos_albaran")
    cantidad_3_num = fields.Float('Cantidad 3', digits = (12, 4), readonly = True, compute = "_get_datos_albaran")
    cantidad_4_num = fields.Float('Cantidad 4', digits = (12, 4), readonly = True, compute = "_get_datos_albaran")
    num_pallets = fields.Integer('Num Pallets', readonly = True, compute = "_get_datos_albaran")
    unidades = fields.Integer('Unidades', readonly = True, compute = "_get_datos_albaran")
    peso_neto = fields.Integer('Peso Neto', readonly = True, compute = "_get_datos_albaran")
    peso_bruto = fields.Integer('Peso Bruto', readonly = True, compute = "_get_datos_albaran")
    numero_contenedor = fields.Char('Numero Contenedor', compute = "_get_datos_albaran")
    precinto_contenedor = fields.Char('Precinto Contenedor', compute = "_get_datos_albaran")
    peso_neto_mojado = fields.Integer('Peso Neto Mojado', compute = "_get_datos_albaran")
    peso_bruto_mojado = fields.Integer('Peso Bruto Mojado', compute = "_get_datos_albaran")
    
    pedido_cliente = fields.Char('Pedido cliente', compute = "_get_datos_pedido")
    carrier_id = fields.Many2one('delivery.carrier', string="Método Entrega", readonly = True, compute = "_get_datos_pedido")

    cantidad = fields.Char('Cantidad', compute = "_get_importe")
    importe = fields.Float('Importe', digits = (10,2), readonly = True, compute = "_get_importe")
    
    fsc_nombre = fields.Char('FSC Nombre', readonly = True, compute = "_get_fsc")
    fsc_venta = fields.Boolean('FSC Venta', readonly = True, compute = "_get_fsc")
    enlaces = fields.Html('Enlaces', readonly = True, compute = "_get_fsc")
    
    vendido = fields.Char('Vendido', readonly = True, compute = '_get_vendido')

    @api.depends('sale_line_ids', 'unidades')
    def _get_vendido(self):
        for record in self:
            vendido = ""
            sale_line_id = None
            for sale in record.sale_line_ids:
                sale_line_id = sale
              
            if sale_line_id != None:
                producto = 0
                if sale_line_id.oferta_id.attribute_id.is_cantonera == True:
                    producto = 1                
                    ala1 = sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_1
                    ala2 = sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_2
                    grosor = sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.grosor_2
                    
                    longitud = sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud
                    #peso = sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.peso_metro
                    metros = record.unidades * longitud / 1000

                    superficie = 0
                    if sale_line_id.oferta_id.attribute_id.cantonera_color_id:
                        superficie = sale_line_id.oferta_id.attribute_id.cantonera_color_id.id
                    
                    vendido = "producto=1" + "&ala1=" + str(ala1) + "&ala2=" + str(ala2) + "&grosor=" + str(grosor) + "&metros=" + str(metros) + "&super=" + str(superficie)
                
                elif sale_line_id.oferta_id.attribute_id.is_slipsheet == True:
                    producto = 3
                    
                    ala1 = sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_1
                    ancho = sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ancho
                    ala2 = sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_2
                    
                    ala3 = sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_3
                    longitud = sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.longitud
                    ala4 = sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.ala_4
                    
                    grosor = sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.grosor_1
                    
                    unidades = record.unidades
                    
                    vendido = "producto=3" + "&ala1=" + str(ala1) + "&ancho=" + str(ancho) + "&ala2=" + str(ala2)
                    vendido = vendido + "&ala3=" + str(ala3) + "&longitud=" + str(longitud) + "&ala4=" + str(ala4)
                    vendido = vendido + "&grosor=" + str(grosor) + "&unidades=" + str(unidades)

            record.vendido = vendido
    
    
    
    @api.depends('sale_line_ids', 'fecha_albaran')
    def _get_fsc(self):
        for record in self:   
            sale_line_id = None
            for sale in record.sale_line_ids:
                sale_line_id = sale

            fsc_nombre = ""
            fsc_venta = False
            enlaces = ""
            if sale_line_id:
                fsc_nombre = sale_line_id.fsc_linea
                if sale_line_id.fsc_valido and sale_line_id.fsc_venta:
                    fsc_venta = True
                    for lote in sale_line_id.lot_ids:
                        enlaces = enlaces + "http://bemecopack.es/jseb/ventafsc_vender.php?pallet=" + lote.name + "&fecha=" + "<br/>"
                
            record.fsc_nombre = fsc_nombre
            record.fsc_venta = fsc_venta
            record.enlaces = enlaces

    @api.depends('precio_num', 'facturar', 'num_pallets', 'cantidad_1_num', 'cantidad_2_num', 'cantidad_3_num', 'cantidad_4_num', 'cantidad_5_num')
    def _get_importe(self):
        for record in self:
            cantidad_num = 0
            cantidad = ''
            importe = 0

            if record.facturar == '1':
                cantidad_num = round(record.cantidad_1_num, 4)
                cantidad = str(cantidad_num) + " metros"
            elif record.facturar == '2':
                cantidad_num = round(record.cantidad_2_num, 4)
                cantidad = str(cantidad_num) + " unidades"
            elif record.facturar == '3':
                cantidad_num = round(record.cantidad_3_num, 4)
                cantidad = str(cantidad_num) + " millares"
            elif record.facturar == '4':
                cantidad_num = round(record.cantidad_4_num, 4)
                cantidad = str(cantidad_num) + " kg"
            elif record.facturar == '5':
                cantidad_num = round(record.cantidad_5_num, 4) 
                cantidad = str(cantidad_num) + " unidades"
  
            importe = cantidad_num * record.precio_num
            
            record.cantidad = cantidad
            record.importe = importe
   
    
    
    @api.depends('move_line_ids', 'facturar', 'cantidad_5_num')
    def _get_datos_albaran(self):
        for record in self:
        
            num_albaran = ''
            fecha_albaran = None
            cantidad_1_num = 0.0
            cantidad_2_num = 0.0
            cantidad_3_num = 0.0
            cantidad_4_num = 0.0
            num_pallets = 0
            unidades = 0
            peso_neto = 0
            peso_bruto = 0
            numero_contenedor = ""
            precinto_contenedor = ""
            peso_neto_mojado = 0
            peso_bruto_mojado = 0
        
            for move in record.move_line_ids:
                num_albaran = num_albaran + move.picking_id.name + ", "
                fecha_albaran = move.picking_id.scheduled_date.date()             
                cantidad_1_num = cantidad_1_num + move.cantidad_1_num
                cantidad_2_num = cantidad_2_num + move.cantidad_2_num
                cantidad_3_num = cantidad_3_num + move.cantidad_3_num
                cantidad_4_num = cantidad_4_num + move.cantidad_4_num
                num_pallets = num_pallets + move.num_pallets
                unidades = unidades + move.unidades
                peso_neto = peso_neto + move.peso_neto
                peso_bruto = peso_bruto + move.peso_bruto
                numero_contenedor = move.picking_id.numero_contenedor
                precinto_contenedor = move.picking_id.precinto_contenedor
                peso_neto_mojado = peso_neto_mojado + move.peso_neto_mojado
                peso_bruto_mojado = peso_bruto_mojado + move.peso_bruto_mojado
            
            if record.facturar == '5':
                unidades = record.cantidad_5_num
                
            record.num_albaran = num_albaran
            record.fecha_albaran = fecha_albaran
            record.cantidad_1_num = cantidad_1_num
            record.cantidad_2_num = cantidad_2_num
            record.cantidad_3_num = cantidad_3_num
            record.cantidad_4_num = cantidad_4_num
            record.num_pallets = num_pallets
            record.unidades = unidades
            record.peso_neto = peso_neto
            record.peso_bruto = peso_bruto
            record.numero_contenedor = numero_contenedor
            record.precinto_contenedor = precinto_contenedor
            record.peso_neto_mojado = peso_neto_mojado
            record.peso_bruto_nojado = peso_bruto_mojado
            
            
    @api.depends('sale_line_ids')
    def _get_datos_pedido(self):
        for record in self:
            pedido_cliente = ''
            for sale in record.sale_line_ids:
                pedido_cliente = sale.order_id.pedido_cliente
                record.carrier_id = sale.order_id.carrier_id.id
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
                precio_num = 0
                precio = ""
                facturar = sale_line_id.oferta_id.attribute_id.referencia_cliente_id.precio_cliente
                cantidad_5_num = 0
                und_pedido = 0
                
                #metros
                if facturar == '1':
                    precio_num = sale_line_id.oferta_id.precio_metro
                    precio_num = round(precio_num, 4)
                    precio = str(precio_num) + " €/metro"
                #unidades
                elif facturar == '2':
                    precio_num = sale_line_id.oferta_id.precio_metro * sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad
                    precio_num = round(precio_num, 4)
                    precio = str(precio_num) + " €/unidad"
                #Millares
                elif facturar == '3':
                    precio_num = sale_line_id.oferta_id.precio_metro * sale_line_id.oferta_id.attribute_id.referencia_cliente_id.referencia_id.metros_unidad * 1000
                    precio_num = round(precio_num, 4)
                    precio = str(precio_num) + " €/millar"
                #Kilos
                elif facturar == '4':
                    precio_num = sale_line_id.oferta_id.precio_kilo
                    precio_num = round(precio_num, 4)
                    precio = str(precio_num) + " €/kilo"
                #Varios
                elif facturar == '5':
                    cantidad_5_num = sale_line_id.und_pallet * sale_line_id.num_pallets
                    precio_num = sale_line_id.oferta_id.precio_varios
                    precio_num = round(precio_num, 4)
                    precio = str(precio_num) + " €/unidad"
                    
                record.codigo_cliente = codigo_cliente
                record.descripcion = descripcion
                record.precio_num = precio_num
                record.precio = precio
                record.facturar = facturar
                record.cantidad_5_num = cantidad_5_num
                
  
