from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

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
                    cantidad_num = sale_line_id.quantity * und_pallet
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
            
            