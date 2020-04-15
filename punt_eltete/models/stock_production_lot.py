
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

from datetime import datetime
import time



class StockProductionInventario(models.Model):
    _name = 'stock.production.inventario'
    
    name = fields.Char(string="Nombre")
    fecha_inicio = fields.Date(string="Fecha Inicio")
    fecha_fin = fields.Date(string="Fecha Fin")
    TIPO_SEL = [ ('10', 'INVENTARIO PRODUCTO TERMINADO HOY'), 
                ('11', 'INVENTARIO PRODUCTO TERMINADO FECHA'), 
                #('20', 'INVENTARIO PAPEL HOY'), 
                #('21', 'INVENTARIO PAPEL FECHA'), 
               ('100', 'PRODUCCIÓN ENTRE FECHAS'), 
               ]
    tipo = fields.Selection(selection = TIPO_SEL, string = 'Tipo', required = True)
    comenzar = fields.Boolean(string="Comenzar Inventario")
    peso_total_bueno = fields.Integer(string="Peso Bueno", readonly = True)
    peso_total_defectuoso = fields.Integer(string="Peso Defectuoso", readonly = True)
    
    peso_cantonera = fields.Integer(string="Peso Cantonera", readonly = True)
    peso_perfilu = fields.Integer(string="Peso Perfil U", readonly = True)
    peso_slipsheet = fields.Integer(string="Peso Slip Sheet", readonly = True)
    peso_formato = fields.Integer(string="Peso Formato", readonly = True)
    peso_bobina = fields.Integer(string="Peso Bobina", readonly = True)
    peso_solidboard = fields.Integer(string="Peso Solid Board", readonly = True)
    peso_pie = fields.Integer(string="Peso Pie Pallet", readonly = True)
    peso_flatboard = fields.Integer(string="Peso Flat Board", readonly = True)
    peso_cantonera_defectuoso = fields.Integer(string="Peso Cantonera Defectuoso", readonly = True)
    peso_perfilu_defectuoso = fields.Integer(string="Peso Perfil U Defectuoso", readonly = True)
    peso_slipsheet_defectuoso = fields.Integer(string="Peso Slip Sheet Defectuoso", readonly = True)
    peso_formato_defectuoso = fields.Integer(string="Peso Formato Defectuoso", readonly = True)
    peso_bobina_defectuoso = fields.Integer(string="Peso Bobina Defectuoso", readonly = True)
    peso_solidboard_defectuoso = fields.Integer(string="Peso Solid Board Defectuoso", readonly = True)
    peso_pie_defectuoso = fields.Integer(string="Peso Pie Pallet Defectuoso", readonly = True)
    peso_flatboard_defectuoso = fields.Integer(string="Peso Flat Board Defectuoso", readonly = True)
    
    lotes_fecha_ids = fields.Many2many('stock.production.lot', readonly = True, string='Lotes Fecha')
    lotes_inventario_ids = fields.Many2many('stock.production.lot', string='Lotes Inventario', compute='_compute_lots')
    
    @api.multi
    def actualizar_inventario(self):
        for record in self:
            peso_cantonera = 0
            peso_perfilu = 0
            peso_slipsheet = 0
            peso_formato = 0
            peso_bobina = 0
            peso_solidboard = 0
            peso_pie = 0
            peso_flatboard = 0
            total_terminado = 0
            
            peso_cantonera_defectuoso = 0
            peso_perfilu_defectuoso = 0
            peso_slipsheet_defectuoso = 0
            peso_formato_defectuoso = 0
            peso_bobina_defectuoso = 0
            peso_solidboard_defectuoso = 0
            peso_pie_defectuoso = 0
            peso_flatboard_defectuoso = 0
            total_terminado_defectuoso = 0
            
            lotes_fecha = None
            
            if record.tipo:
                if record.tipo == '10':
                    #Inventario producto terminado HOY
                    for lote in self.env['stock.production.lot'].search([('is_mprima_papel', '=', False),('is_varios', '=', False),]):
                        if record.comenzar == True:
                            lote.inventariado = False
                            
                        if lote.fecha_entrada == None or lote.fecha_entrada == False:
                            lote.almacenado = False
                        elif lote.date_done == None or lote.date_done == False:
                            lote.fecha_salir = None
                            lote.almacenado = True
                        else:
                            lote.fecha_salir = lote.scheduled_date
                            lote.almacenado = False

                        if lote.almacenado == True:
                            
                            if lote.is_cantonera == True:
                                if lote.defectuoso == True:
                                    peso_cantonera_defectuoso = peso_cantonera_defectuoso + lote.peso_neto
                                    total_terminado_defectuoso = total_terminado_defectuoso + lote.peso_neto
                                else:
                                    peso_cantonera = peso_cantonera + lote.peso_neto
                                    total_terminado = total_terminado + lote.peso_neto
                            if lote.is_perfilu == True:
                                if lote.defectuoso == True:
                                    peso_perfilu_defectuoso = peso_perfilu_defectuoso + lote.peso_neto
                                    total_terminado_defectuoso = total_terminado_defectuoso + lote.peso_neto
                                else:
                                    peso_perfilu = peso_perfilu + lote.peso_neto
                                    total_terminado = total_terminado + lote.peso_neto
                            if lote.is_slipsheet == True:
                                if lote.defectuoso == True:
                                    peso_slipsheet_defectuoso = peso_slipsheet_defectuoso + lote.peso_neto
                                    total_terminado_defectuoso = total_terminado_defectuoso + lote.peso_neto
                                else:
                                    peso_slipsheet = peso_slipsheet + lote.peso_neto
                                    total_terminado = total_terminado + lote.peso_neto
                            if lote.is_formato == True:
                                if lote.defectuoso == True:
                                    peso_formato_defectuoso = peso_formato_defectuoso + lote.peso_neto
                                    total_terminado_defectuoso = total_terminado_defectuoso + lote.peso_neto
                                else:
                                    peso_formato = peso_formato + lote.peso_neto
                                    total_terminado = total_terminado + lote.peso_neto
                            if lote.is_bobina == True:
                                if lote.defectuoso == True:
                                    peso_bobina_defectuoso = peso_bobina_defectuoso + lote.peso_neto
                                    total_terminado_defectuoso = total_terminado_defectuoso + lote.peso_neto
                                else:
                                    peso_bobina = peso_bobina + lote.peso_neto
                                    total_terminado = total_terminado + lote.peso_neto
                            if lote.is_solidboard == True:
                                if lote.defectuoso == True:
                                    peso_solidboard_defectuoso = peso_solidboard_defectuoso + lote.peso_neto
                                    total_terminado_defectuoso = total_terminado_defectuoso + lote.peso_neto
                                else:
                                    peso_solidboard = peso_solidboard + lote.peso_neto
                                    total_terminado = total_terminado + lote.peso_neto
                            if lote.is_pieballet == True:
                                if lote.defectuoso == True:
                                    peso_pie_defectuoso = peso_pie_defectuoso + lote.peso_neto
                                    total_terminado_defectuoso = total_terminado_defectuoso + lote.peso_neto
                                else:
                                    peso_pie = peso_pie + lote.peso_neto
                                    total_terminado = total_terminado + lote.peso_neto
                            if lote.is_flatboard == True:
                                if lote.defectuoso == True:
                                    peso_flatboard_defectuoso = peso_flatboard_defectuoso + lote.peso_neto
                                    total_terminado_defectuoso = total_terminado_defectuoso + lote.peso_neto
                                else:
                                    peso_flatboard = peso_flatboard + lote.peso_neto
                                    total_terminado = total_terminado + lote.peso_neto
                                
                elif record.tipo == '11' and record.fecha_fin:
                    #Inventario Producto Terminado fecha
                    for lote in self.env['stock.production.lot'].search([('is_mprima_papel', '=', False),('is_varios', '=', False),]):

                        if lote.fecha_entrada == None or lote.fecha_entrada == False:
                            lote.almacenado_fecha = False
                        elif lote.fecha_entrada <= record.fecha_fin:
                            if lote.date_done == None or lote.date_done == False:
                                lote.fecha_salir = None
                                lote.almacenado_fecha = True
                            else:
                                lote.fecha_salir = lote.scheduled_date
                                if lote.fecha_salir > record.fecha_fin:
                                    lote.almacenado_fecha = True
                                else:
                                    lote.almacenado_fecha = False
                        else:
                            lote.almacenado_fecha = False

                        if lote.almacenado_fecha == True:  
                            
                            if lote.is_cantonera == True:
                                if lote.defectuoso == True:
                                    peso_cantonera_defectuoso = peso_cantonera_defectuoso + lote.peso_neto
                                    total_terminado_defectuoso = total_terminado_defectuoso + lote.peso_neto
                                else:
                                    peso_cantonera = peso_cantonera + lote.peso_neto
                                    total_terminado = total_terminado + lote.peso_neto
                            if lote.is_perfilu == True:
                                if lote.defectuoso == True:
                                    peso_perfilu_defectuoso = peso_perfilu_defectuoso + lote.peso_neto
                                    total_terminado_defectuoso = total_terminado_defectuoso + lote.peso_neto
                                else:
                                    peso_perfilu = peso_perfilu + lote.peso_neto
                                    total_terminado = total_terminado + lote.peso_neto
                            if lote.is_slipsheet == True:
                                if lote.defectuoso == True:
                                    peso_slipsheet_defectuoso = peso_slipsheet_defectuoso + lote.peso_neto
                                    total_terminado_defectuoso = total_terminado_defectuoso + lote.peso_neto
                                else:
                                    peso_slipsheet = peso_slipsheet + lote.peso_neto
                                    total_terminado = total_terminado + lote.peso_neto
                            if lote.is_formato == True:
                                if lote.defectuoso == True:
                                    peso_formato_defectuoso = peso_formato_defectuoso + lote.peso_neto
                                    total_terminado_defectuoso = total_terminado_defectuoso + lote.peso_neto
                                else:
                                    peso_formato = peso_formato + lote.peso_neto
                                    total_terminado = total_terminado + lote.peso_neto
                            if lote.is_bobina == True:
                                if lote.defectuoso == True:
                                    peso_bobina_defectuoso = peso_bobina_defectuoso + lote.peso_neto
                                    total_terminado_defectuoso = total_terminado_defectuoso + lote.peso_neto
                                else:
                                    peso_bobina = peso_bobina + lote.peso_neto
                                    total_terminado = total_terminado + lote.peso_neto
                            if lote.is_solidboard == True:
                                if lote.defectuoso == True:
                                    peso_solidboard_defectuoso = peso_solidboard_defectuoso + lote.peso_neto
                                    total_terminado_defectuoso = total_terminado_defectuoso + lote.peso_neto
                                else:
                                    peso_solidboard = peso_solidboard + lote.peso_neto
                                    total_terminado = total_terminado + lote.peso_neto
                            if lote.is_pieballet == True:
                                if lote.defectuoso == True:
                                    peso_pie_defectuoso = peso_pie_defectuoso + lote.peso_neto
                                    total_terminado_defectuoso = total_terminado_defectuoso + lote.peso_neto
                                else:
                                    peso_pie = peso_pie + lote.peso_neto
                                    total_terminado = total_terminado + lote.peso_neto
                            if lote.is_flatboard == True:
                                if lote.defectuoso == True:
                                    peso_flatboard_defectuoso = peso_flatboard_defectuoso + lote.peso_neto
                                    total_terminado_defectuoso = total_terminado_defectuoso + lote.peso_neto
                                else:
                                    peso_flatboard = peso_flatboard + lote.peso_neto
                                    total_terminado = total_terminado + lote.peso_neto
                                    
                    lotes_fecha = self.env['stock.production.lot'].search([('is_mprima_papel', '=', False),('is_varios', '=', False),('almacenado_fecha', '=', True),])
                
                elif record.tipo == '100' and record.fecha_inicio and record.fecha_fin:
                    #Producción entre FECHAS
                    for lote in self.env['stock.production.lot'].search([('is_mprima_papel', '=', False),('is_varios', '=', False),('is_perfilu', '=', False),('is_formato', '=', False),('is_bobina', '=', False),('is_pieballet', '=', False),('is_flatboard', '=', False),]):
                        
                        if lote.fecha_entrada == None or lote.fecha_entrada == False:
                            lote.almacenado_fecha = False
                        elif lote.fecha_entrada >= record.fecha_inicio and lote.fecha_entrada <= record.fecha_fin:
                            lote.almacenado_fecha = True
                        else:
                            lote.almacenado_fecha = False
                                    
                        if lote.almacenado_fecha == True:  
                            
                            if lote.is_cantonera == True:
                                if lote.defectuoso == True:
                                    peso_cantonera_defectuoso = peso_cantonera_defectuoso + lote.peso_neto
                                    total_terminado_defectuoso = total_terminado_defectuoso + lote.peso_neto
                                else:
                                    peso_cantonera = peso_cantonera + lote.peso_neto
                                    total_terminado = total_terminado + lote.peso_neto
                            if lote.is_slipsheet == True:
                                if lote.defectuoso == True:
                                    peso_slipsheet_defectuoso = peso_slipsheet_defectuoso + lote.peso_neto
                                    total_terminado_defectuoso = total_terminado_defectuoso + lote.peso_neto
                                else:
                                    peso_slipsheet = peso_slipsheet + lote.peso_neto
                                    total_terminado = total_terminado + lote.peso_neto
                            if lote.is_solidboard == True:
                                if lote.defectuoso == True:
                                    peso_solidboard_defectuoso = peso_solidboard_defectuoso + lote.peso_neto
                                    total_terminado_defectuoso = total_terminado_defectuoso + lote.peso_neto
                                else:
                                    peso_solidboard = peso_solidboard + lote.peso_neto
                                    
                    lotes_fecha = self.env['stock.production.lot'].search([('is_mprima_papel', '=', False),('is_varios', '=', False),('is_perfilu', '=', False),('is_formato', '=', False),('is_bobina', '=', False),('is_pieballet', '=', False),('is_flatboard', '=', False),('almacenado_fecha', '=', True),])
                
            record.peso_cantonera = peso_cantonera
            record.peso_perfilu = peso_perfilu
            record.peso_slipsheet = peso_slipsheet
            record.peso_formato = peso_formato
            record.peso_bobina = peso_bobina
            record.peso_solidboard = peso_solidboard
            record.peso_pie = peso_pie
            record.peso_flatboard = peso_flatboard
            record.peso_cantonera_defectuoso = peso_cantonera_defectuoso
            record.peso_perfilu_defectuoso = peso_perfilu_defectuoso
            record.peso_slipsheet_defectuoso = peso_slipsheet_defectuoso
            record.peso_formato_defectuoso = peso_formato_defectuoso
            record.peso_bobina_defectuoso = peso_bobina_defectuoso
            record.peso_solidboard_defectuoso = peso_solidboard_defectuoso
            record.peso_pie_defectuoso = peso_pie_defectuoso
            record.peso_flatboard_defectuoso = peso_flatboard_defectuoso
            record.peso_total_bueno = total_terminado
            record.peso_total_defectuoso = total_terminado_defectuoso
            
            record.lotes_fecha_ids = lotes_fecha
            record.comenzar = False
                    
    
    
    @api.depends('tipo')
    def _compute_lots(self):
        for record in self:
            inventario = None
            if record.tipo:
                if record.tipo == '10':
                    inventario1 = self.env['stock.production.lot'].search([('is_mprima_papel', '=', False),('almacenado', '=', True),('inventariado', '=', False)])
                    inventario2 = self.env['stock.production.lot'].search([('is_mprima_papel', '=', False),('almacenado', '=', False),('inventariado', '=', True)])
                    inventario = inventario1 + inventario2
            
            record.lotes_inventario_ids = inventario




class StockProductionSuperorden(models.Model):
    _name = 'stock.production.superorden'
    
    name = fields.Char(string="Nombre")
    sale_line_ids = fields.One2many('sale.order.line', 'superorden_id', string="Líneas de Pedidos")
    consumo_ids = fields.One2many('stock.production.lot.consumo', 'superorden_id', string="Consumos")
    lot_ids = fields.One2many('stock.production.lot', 'superorden_id', string="Lotes Salida")




class StockProductionLotConsumo(models.Model):
    _name = 'stock.production.lot.consumo'
    
    name = fields.Char(string="Nombre")
    lot_id = fields.Many2one('stock.production.lot', string = "Lote")
    superorden_id = fields.Many2one('stock.production.superorden', string="Superorden")
    fecha_entrada = fields.Datetime('Fecha Entrada')
    peso_bruto_entrada = fields.Float('Peso Bruto Entrada', digits = (10, 2))
    fecha_salida = fields.Datetime('Fecha Salida')
    peso_bruto_salida = fields.Float('Peso Bruto Salida', digits = (10, 2))
    
    
    
class StockProductionTrabajador(models.Model):
    _name = 'stock.production.trabajador'
    
    name = fields.Char(string="Name", readonly = True, compute = "_get_nombre")
    numero = fields.Integer('Número')
    nombre = fields.Char(string="Nombre")
    apellidos = fields.Char(string="Apellidos")
    dni = fields.Char(string="DNI")
    telefono = fields.Char(string="Teléfono")
    active = fields.Boolean("Activo", default = True)
    
    @api.depends('numero', 'nombre', 'apellidos')
    def _get_nombre(self):
        for record in self:
            nombre = ""
            if record.numero > 0:
                if record.numero < 10:
                    nombre = "0"
                nombre = nombre + str(record.numero) + " "
            if record.nombre:
                nombre = nombre + record.nombre
                if record.apellidos:
                    nombre = nombre + " " + record.apellidos
            record.name = nombre
    
    
class StockProductionLotCalidad(models.Model):
    _name = 'stock.production.lot.calidad'
    
    lot_id = fields.Many2one('stock.production.lot', string = "Lote")
    fecha = fields.Datetime('Fecha')
    trabajador_id = fields.Many2one('stock.production.trabajador', string = "Trabajador")
    ala_1 = fields.Float('Ala 1', digits=(10,2))
    ala_2 = fields.Float('Ala 2', digits=(10,2))
    grosor_1 = fields.Float('Grosor 1', digits=(10,2))
    grosor_2 = fields.Float('Grosor 2', digits=(10,2))
    longitud = fields.Integer('Longitud')
       
    
    





class StockProductionLotOperario(models.Model):
    _name = 'stock.production.lot.operario'
    
    trabajador = fields.Integer('Trabajador', required = True)
    trabajador_id = fields.Many2one('stock.production.trabajador', string = "Trabajador")
    operario_id = fields.Many2one('hr.employee', string = "Empleado")
    lot_id = fields.Many2one('stock.production.lot', string = "Lote")
    MAQUINA_SEL = [ ('CA1', 'CANTONERA 1'), 
               ('CA2', 'CANTONERA 2'), 
               ('CA3', 'CANTONERA 3'), 
               ('CA4', 'CANTONERA 4'), 
               ('SS1', 'CONTRACOLADORA 1'), 
               ('SI1', 'SIERRA 1'), 
               ('TR1', 'TROQUELADORA 1'), 
               ]
    maquina = fields.Selection(selection = MAQUINA_SEL, string = 'Máquina')
    TAREA_SEL = [ ('FAB', 'FABRICACIÓN'), 
               ('CAM', 'CAMBIO'), 
               ('PAL', 'PALETIZADO'), 
               ('IMP', 'PREPARAR IMPRESIÓN'),
               ('AV1', 'AVERIA MÁQUINA'),
               ]
    tarea = fields.Selection(selection = TAREA_SEL, string = 'Tarea', required = True)
    fecha_inicio = fields.Datetime('Fecha Inicio')
    und_inicio = fields.Integer(string="Und inicio", default = 1)
    fecha_fin = fields.Datetime('Fecha Fin')
    und_fin = fields.Integer(string="Und Fin")
    metros = fields.Float('Metros', digits = (10, 2), readonly = True, compute = "_get_produccion")
    kilos = fields.Float('Kilos', digits = (10, 2), readonly = True, compute = "_get_produccion")
    
    minutos = fields.Integer(string="Minutos", compute = "_get_minutos")
    
    #hora_inicio = fields.Float(string = "Hora inicio")
    #<field name='hora_inicio' widget="float_time"/>
    
    @api.depends('fecha_inicio', 'fecha_fin')
    def _get_minutos(self):
        for record in self:
            if record.fecha_inicio and record.fecha_fin:
                fmt = '%Y-%m-%d %H:%M:%S'
                #d1 = datetime.strptime(record.fecha_inicio, fmt)
                #d2 = datetime.strptime(record.fecha_fin, fmt)
                
                d1 = record.fecha_inicio
                d2 = record.fecha_fin

                d1_ts = time.mktime(d1.timetuple())
                d2_ts = time.mktime(d2.timetuple())


                record.minutos = int(d2_ts-d1_ts) / 60


   
    
    @api.depends('und_inicio', 'und_fin', 'lot_id.referencia_id')
    def _get_produccion(self):
        for record in self:
            metros = 0
            kilos = 0
            if record.lot_id:
                if record.lot_id.referencia_id and record.tarea == 'FAB':
                    if record.und_inicio > 0 and record.und_fin > 0 and record.und_fin > record.und_inicio:
                        unidades = record.und_fin - record.und_inicio + 1
                        metros = unidades * record.lot_id.referencia_id.metros_unidad
                        kilos = metros * record.lot_id.referencia_id.peso_metro
         
            record.metros = metros
            record.kilos = kilos
        
        

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    picking_id = fields.Many2one('stock.picking', string = "Albarán", compute = "_get_datos_albaran")
    scheduled_date = fields.Date(string = "Fecha prevista", compute = "_get_datos_albaran", readonly=True)
    date_done = fields.Datetime(string = "Fecha efectiva", compute = "_get_datos_albaran", readonly=True)
    sale_order_line_id = fields.Many2one('sale.order.line', string = "Línea Pedido Venta")
    referencia_id = fields.Many2one('product.referencia', string="Referencia")
    cliente_id = fields.Many2one('res.partner', string="Cliente", store=False, related='sale_order_id.partner_id')
    cliente_ref = fields.Char('Rerencia Cliente', readonly = True, store=False, compute = "_get_cliente")
    sale_order_id = fields.Many2one('sale.order', string='Pedido Venta', store=True, related='sale_order_line_id.order_id', readonly=True)
    operario_ids = fields.One2many('stock.production.lot.operario', 'lot_id', string="Operarios")
    
    purchase_order_line_id = fields.Many2one('purchase.order.line', string = "Línea Pedido Compra")
    purchase_order_id = fields.Many2one('purchase.order', string='Pedido Compra', store=True, related='purchase_order_line_id.order_id', readonly=True)
    
    metido = fields.Boolean('Metido', readonly = True, compute = "_get_metido")
    fecha_entrada = fields.Date('Fecha Entrada')
    fecha_salir = fields.Date('Fecha Salida', readonly = True)
    almacen = fields.Boolean('Almacen', readonly = True, compute = "_get_disponible")
    disponible = fields.Boolean('Disponible', readonly = True, store = True, compute = "_get_disponible")
    unidades = fields.Integer('Unidades')
    peso_neto = fields.Integer('Peso Neto', readonly = True, compute = "_get_peso")
    peso_bruto = fields.Integer('Peso Bruto', readonly = True, compute = "_get_peso")
    user_peso_bruto = fields.Float('User Peso Bruto', digits=(10, 2))
    user_peso_neto = fields.Float('User Peso Neto', digits=(10, 2))
    peso_metro = fields.Float('Peso Metro', readonly = True, digits=(12, 4), compute = "_get_peso" )
    
    imprimir_etiqueta = fields.Boolean('Imprimir Etiqueta', compute = "_get_etiqueta")
    descripcion = fields.Html('Descripcion')
    dir_qr = fields.Char('Dir QR', readonly = True, compute = "_get_dir_qr")
    defectuoso = fields.Boolean('Defectuoso')
    comentario = fields.Char('Comentario')

    cantidad_1 = fields.Char('Cantidad 1', readonly = True, compute = "_get_cantidad")
    cantidad_2 = fields.Char('Cantidad 2', readonly = True, compute = "_get_cantidad")
    cantidad_3 = fields.Char('Cantidad 3', readonly = True, compute = "_get_cantidad")
    cantidad_4 = fields.Char('Cantidad 4', readonly = True, compute = "_get_cantidad")
    
    cantidad_1_num = fields.Float('Cantidad 1', digits = (12, 4), readonly = True, compute = "_get_cantidad")
    cantidad_2_num = fields.Float('Cantidad 2', digits = (12, 4), readonly = True, compute = "_get_cantidad")
    cantidad_3_num = fields.Float('Cantidad 3', digits = (12, 4), readonly = True, compute = "_get_cantidad")
    cantidad_4_num = fields.Float('Cantidad 4', digits = (12, 4), readonly = True, compute = "_get_cantidad")
    
    almacenado = fields.Boolean('Almacenado')
    almacenado_fecha = fields.Boolean('Almacenado Fecha')
    inventariado = fields.Boolean('Inventariado')
    #und_paquete = fields.Integer('Und paquete')
    comprado = fields.Boolean('Comprado')
    fabricat = fields.Boolean('Fabricado', default = True)

    superorden_id = fields.Many2one('stock.production.superorden', string="Superorden")
    consumo_ids = fields.One2many('stock.production.lot.consumo', 'lot_id', string="Consumos")
    calidad_ids  = fields.One2many('stock.production.lot.calidad', 'lot_id', string="Calidad")
    
    
    @api.multi
    def name_get(self):
        res = super(StockProductionLot, self).name_get()
        data = []
        for lot in self:
            display_value = lot.name
            if lot.unidades > 0:
                display_value = display_value + ' (' + str(lot.unidades) + ')'
            data.append((lot.id, display_value))
        return data

    
    #PARA CREAR EL LOTE SIN ORDEN DE PRODUCCIÓN
    type_id = fields.Many2one('product.category', string="Tipo de producto", required=True)
    is_cantonera = fields.Boolean('¿Es Cantonera?', related='type_id.is_cantonera')
    is_perfilu = fields.Boolean('¿Es Perfil U?', related='type_id.is_perfilu')
    is_slipsheet = fields.Boolean('¿Es Slip Sheet?', related='type_id.is_slipsheet')
    is_solidboard = fields.Boolean('¿Es Solid Board?', related='type_id.is_solidboard')
    is_formato = fields.Boolean('¿Es Formato?', related='type_id.is_formato')
    is_bobina = fields.Boolean('¿Es Bobina?', related='type_id.is_bobina')
    is_pieballet = fields.Boolean('¿Es Pie de Ballet?', related='type_id.is_pieballet')
    is_varios = fields.Boolean('¿Es Varios?', related='type_id.is_varios')
    is_flatboard = fields.Boolean('¿Es Flat Board?', related='type_id.is_flatboard')
    is_mprima_papel = fields.Boolean('¿Es mPrima Papel?', related='type_id.is_mprima_papel')
    
    TIPO_PIE = [('1', 'Alto 100 con Adhesivo'), 
               ('2', 'Alto 100 sin Adhesivo'),
               ('3', 'Alto 60 con Adhesivo'),                 
               ('4', 'Alto 60 sin Adhesivo'),        
               ]
    pie = fields.Selection(selection = TIPO_PIE, string = 'Tipo Pie', default = '1')
    ala_1 = fields.Integer('Ala 1 / Solapa')
    ancho = fields.Integer('Ancho')
    ala_2 = fields.Integer('Ala 2')
    grosor_2 = fields.Float('Grosor 2', digits=(8,2))
    ala_3 = fields.Integer('Solapa 3')
    longitud = fields.Integer('Longitud')
    ala_4 = fields.Integer('Solapa 4')
    grosor_1 = fields.Float('Grosor 1', digits=(8,1))    
    diametro = fields.Integer('Diámetro')
    gramaje = fields.Integer('Gramaje')
    tipo_varios_id = fields.Many2one('product.caracteristica.varios', string="Tipo varios")
    
    barras_1_imagen = fields.Char('Barras 1 Imagen', readonly = True, compute = "_get_barras")
    barras_1_texto = fields.Char('Barras 1 Texto', readonly = True, compute = "_get_barras")
    barras_2_imagen = fields.Char('Barras 2 Imagen', readonly = True, compute = "_get_barras")
    barras_2_texto = fields.Char('Barras 2 Texto', readonly = True, compute = "_get_barras")
    barras_3_imagen = fields.Char('Barras 3 Imagen', readonly = True, compute = "_get_barras")
    barras_3_texto = fields.Char('Barras 3 Texto', readonly = True, compute = "_get_barras")
    
    
    
    @api.depends('unidades')
    def _get_barras(self):
        for record in self:
            barras_1_imagen = ""
            barras_1_texto = ""
            barras_2_imagen = ""
            barras_2_texto = ""
            barras_3_imagen = ""
            barras_3_texto = ""
            
            #Buscamnos los datos en el name
            guardar_orden = False
            guardar_pallet = False
            orden = ""
            pallet = ""
            indice = 0
            while indice < len(record.name):
                letra = record.name[indice, indice + 1]
                if letra == "-":
                    if orden == "":
                        guardar_orden = True
                    elif pallet == "-":
                        guardar_orden = False
                        guardar_pallet = True
                elif letra == " ":
                    x = 0
                else:
                    if guardar_orden == True:
                        orden = orden + letra
                    elif guarda_pallet == True:
                        pallet = pallet + letra       
                indice = indice + 1
            
            #Barras 1
            barras_1_imagen = "91"
            barras_1_texto = "(91)"
            #Añadimos el IPMS
            if record.longitud == 710:
                barras_1_imagen = barras_1_imagen + "91286481"
                barras_1_texto = barras_1_texto + "91286481"
            elif record.longitud == 805:
                barras_1_imagen = barras_1_imagen + "91056758"
                barras_1_texto = barras_1_texto + "91056758"
            else:
                barras_1_imagen = barras_1_imagen + "00000000"
                barras_1_texto = barras_1_texto + "00000000"
                
            barras_1_imagen = barras_1_imagen + "37"
            barras_1_texto = barras_1_texto + "(37)"
            #Añadimos las unidades (8 digitos)
            codigo = str(record.unidades)
            while len(codigo) < 8:
                codigo = "0" + codigo
                
            barras_1_imagen = barras_1_imagen + codigo
            barras_1_texto = barras_1_texto + codigo
            
            #Barras 2
            barras_2_imagen = "10ELBU"
            barras_2_texto = "(10)ELBU"
            #Insertamos la orden de produccion (max 10 digitos, mínimo 6)
            while len(orden) < 6:
                orden = "0" + orden
            
            barras_2_imagen = barras_2_imagen + orden + " 90EU"
            barras_2_texto = barras_2_texto + orden + "(90)EU"
            
            #Barras 3
            barras_3_imagen = "0018406608" + orden
            barras_3_texto = "(00)18406608" + orden
            #Insertamos número de pallet (maximo 3 digitos)
            while len(pallet) < 3:
                pallet = "0" + pallet
            barras_3_imagen = barras_3_imagen + pallet
            barras_3_texto = barras_3_texto + pallet
            
            #Codigo de control
            indice = 10
            valor = 55
            impar = True
            while indice < len(barras_3_imagen):
                numero = int(barras_3_imagen[indice, indice + 1])
                if impar == True:
                    valor = valor + numero * 3
                    impar = False
                else:
                    valor = valor + numero
                    impar = True
                indice = indice + 1
            
            decena_mayor = (int(valor / 10) + 1) * 10
            control = decena_mayor - valor
            if control == 10:
                control = 0
            
            barras_3_imagen = barras_3_imagen + str(control)
            barras_3_texto = barras_3_texto + str(control)
            
            record.barras_1_imagen = barras_1_imagen
            record.barras_1_texto = barras_1_texto
            record.barras_2_imagen = barras_2_imagen
            record.barras_2_texto = barras_2_texto
            record.barras_3_imagen = barras_3_imagen
            record.barras_3_texto = barras_3_texto
    
    

    
    @api.depends('comprado', 'sale_order_line_id')
    def _get_etiqueta(self):
        for record in self:
            cambiar = False
            if record.comprado == True:
                cambiar = True
            if record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.unidades != record.unidades:
                    cambiar = True

            record.imprimir_etiqueta = cambiar
          
        
    @api.depends('name')
    def _get_dir_qr(self):
        for record in self:
            if record.name:
                if record.is_mprima_papel == True:
                    dir_qr = "http://bemecopack.es/jseb/qr_lote.php?papel="
                else:
                    dir_qr = "http://bemecopack.es/jseb/qr_lote.php?pallet="
                dir_qr = dir_qr + record.name           

            record.dir_qr = dir_qr


    @api.onchange('type_id',)
    def _onchange_type_id(self):
        if self.type_id.is_cantonera == True:
            self.comprado = False
            self.fabricat = True
        if self.type_id.is_perfilu == True:
            self.comprado = True
            self.fabricat = False
        if self.type_id.is_slipsheet == True:
            self.comprado = False
            self.fabricat = True
        if self.type_id.is_formato == True:
            self.comprado = True
            self.fabricat = False
        if self.type_id.is_bobina == True:
            self.comprado = True
            self.fabricat = False
        if self.type_id.is_pieballet == True:
            self.comprado = True
            self.fabricat = False
        if self.type_id.is_flatboard == True:
            self.comprado = True
            self.fabricat = False
        if self.type_id.is_varios == True:
            self.comprado = False
            self.fabricat = False
        if self.type_id.is_mprima_papel == True:
            self.comprado = True
            self.fabricat = False
            
    
    @api.onchange('sale_order_line_id')
    def _onchange_linea_pedido(self):
        if self.sale_order_line_id:
            self.descripcion = self.sale_order_line_id.descripcion
    
    
    @api.depends('operario_ids')
    def _get_metido(self):
        for record in self:
            metido = False
            if len(record.operario_ids) > 0:
                metido = True
            
            record.metido = metido
    
    
    
    @api.depends('cliente_id')
    def _get_cliente(self):
        for record in self:
            cliente_ref = ""
            if record.cliente_id:
                cliente_ref = record.cliente_id.ref
            
            record.cliente_ref = cliente_ref
    

    @api.depends('sale_order_line_id', 'fecha_entrada', 'date_done', 'scheduled_date', 'defectuoso')
    def _get_disponible(self):
        for record in self:
            disponible = False
            almacen = False
            #fecha_salida = None
            if record.fecha_entrada:
                disponible = True
                almacen = True
                if record.defectuoso == True:
                    disponible = False
                elif record.sale_order_line_id:
                    disponible = False
                    if record.date_done and record.scheduled_date:
                        almacen = False
                        #fecha_salida = record.scheduled_date
                     
            record.disponible = disponible
            record.almacen = almacen
            #record.fecha_salir = fecha_salida
    
    
    
    @api.depends('sale_order_line_id', 'sale_order_line_id.move_ids', 'sale_order_line_id.move_ids.move_line_ids.lot_id')
    def _get_datos_albaran(self):
        for record in self:
            picking_id = None
            scheduled_date = None
            date_done = None
            for move in record.sale_order_line_id.move_ids:
                for line in move.move_line_ids:
                    if line.lot_id:
                        if line.lot_id.id == record.id:
                            picking_id = move.picking_id.id
                            date_done = move.picking_id.date_done
                            scheduled_date  = move.picking_id.scheduled_date.date()
                            
            record.picking_id = picking_id
            record.scheduled_date = scheduled_date
            record.date_done = date_done
            
    
    
    @api.depends('unidades', 'peso_neto')
    def _get_cantidad(self):
        for record in self:
            cantidad_1 = record.referencia_id.metros_unidad * record.unidades
            cantidad_2 = record.unidades
            cantidad_3 = record.unidades / 1000
            cantidad_4 = record.peso_neto
            
            cantidad_1 = round(cantidad_1, 4)
            cantidad_2 = round(cantidad_2, 4)
            cantidad_3 = round(cantidad_3, 4)
            cantidad_4 = round(cantidad_4, 4)
            
            record.cantidad_1_num = cantidad_1
            record.cantidad_2_num = cantidad_2
            record.cantidad_3_num = cantidad_3
            record.cantidad_4_num = cantidad_4
            
            record.cantidad_1 = str(cantidad_1)
            record.cantidad_2 = str(cantidad_2)
            record.cantidad_3 = str(cantidad_3)
            record.cantidad_4 = str(cantidad_4)


    """
    #CANTONERA
    cantonera_color_id = fields.Char('Cantonera Color', readonly = True, compute = "_get_valores")
    cantonera_forma_id = fields.Many2one('product.caracteristica.cantonera.forma', string="Forma", readonly = True, compute = "_get_valores")
    cantonera_especial_id = fields.Many2one('product.caracteristica.cantonera.especial', string="Especial", readonly = True, compute = "_get_valores")
    cantonera_impresion_id = fields.Many2one('product.caracteristica.cantonera.impresion', string="Impresión", readonly = True, compute = "_get_valores")
    cantonera_cliche_id = fields.Many2one('product.caracteristica.cliche', string="Cliché", readonly = True, compute = "_get_valores")
    fsc_id = fields.Many2one('product.caracteristica.fsc', string = "FSC", readonly = True, compute = "_get_valores")
    reciclable_id = fields.Many2one('product.caracteristica.reciclable', string = "Reciclable", readonly = True, compute = "_get_valores")
    paletizado = fields.Integer('Paletizado', compute="_get_valores")
    
    user_cantonera_color_id = fields.Many2one('product.caracteristica.cantonera.color', string="Cambiar Cantonera Color")
    user_cantonera_forma_id = fields.Many2one('product.caracteristica.cantonera.forma', string="Cambiar Forma")
    user_cantonera_especial_id = fields.Many2one('product.caracteristica.cantonera.especial', string="Cambiar Especial")
    user_cantonera_impresion_id = fields.Many2one('product.caracteristica.cantonera.impresion', string="Cambiar Impresión")
    user_cantonera_cliche_id = fields.Many2one('product.caracteristica.cliche', string="Cambiar Cliché")
    user_fsc_id = fields.Many2one('product.caracteristica.fsc', string = "Cambiar FSC")
    user_reciclable_id = fields.Many2one('product.caracteristica.reciclable', string = "Cambiar Reciclable")
    PALETIZADO_SEL = [('1', 'Compacto (Normal)'),                 
                      ('2', 'Columnas'),
                      ]
    user_paletizado = fields.Selection(selection = PALETIZADO_SEL, string = 'Paletizado')
    
    
    #PERFILU
    perfilu_color_id = fields.Many2one('product.caracteristica.perfilu.color', string="Perfil U Color", readonly = True, compute = "_get_valores")
    
    user_perfilu_color_id = fields.Many2one('product.caracteristica.perfilu.color', string="Cambiar Perfil U Color")
    
    #CANTONERA Y PERFILU
    inglete_id = fields.Many2one('product.caracteristica.inglete', string = "Tipo Inglete", readonly = True, compute = "_get_valores")
    inglete_num = fields.Integer('Numero de Ingletes', readonly = True, compute = "_get_valores")
    inglete_texto = fields.Char('Inglete Descripcion', readonly = True, compute = "_get_valores")
    
    user_inglete_id = fields.Many2one('product.caracteristica.inglete', string = "Cambiar Tipo Inglete")
    user_inglete_num = fields.Integer('Cambiar Numero de Ingletes')
    user_inglete_texto = fields.Char('Cambiar Inglete Descripcion')
    
    
    #SOLID BOARD
    plancha_color_id = fields.Many2one('product.caracteristica.planchacolor', string = "Plancha Color", readonly = True, compute = "_get_valores")
    
    user_plancha_color_id = fields.Many2one('product.caracteristica.planchacolor', string = "Cambiar Plancha Color")
    
    
    #FORMATO Y BOBINA
    papel_calidad_id = fields.Many2one('product.caracteristica.papelcalidad', string = "Papel Calidad", readonly = True, compute = "_get_valores")
    
    user_papel_calidad_id = fields.Many2one('product.caracteristica.papelcalidad', string = "Cambiar Papel Calidad")
    
    
    #SLIPSHEET, SOLIDBOARD Y FORMATO
    troquelado_id = fields.Many2one('product.caracteristica.troquelado', string = "Troquelado", readonly = True, compute = "_get_valores")
    
    user_troquelado_id = fields.Many2one('product.caracteristica.troquelado', string = "Cambiar Troquelado")
    
    """


    @api.depends('referencia_id', 'unidades', 'user_peso_neto', 'user_peso_bruto')
    def _get_peso(self):
        for record in self:
            peso_neto = 0
            peso_bruto = 0
            peso_metro = 0
            if record.user_peso_neto > 0:
                peso_neto = record.user_peso_neto
                peso_bruto = record.user_peso_neto + 10
            elif record.user_peso_bruto > 0:
                peso_neto = record.user_peso_bruto - 10
                peso_bruto = record.user_peso_bruto
            elif record.referencia_id and record.unidades > 0:
                peso_metro = record.referencia_id.peso_metro
                peso_und = peso_metro * record.referencia_id.metros_unidad
                peso_neto = peso_und * record.unidades
                
                pesoMadera = 0
                if record.referencia_id.longitud < 1500:
                    pesoMadera = 15
                elif record.referencia_id.longitud < 2000:
                    pesoMadera = 20
                else:
                    pesoMadera = int(record.referencia_id.longitud / 1000) * 15  
                peso_bruto = int((peso_neto + pesoMadera) / 5) * 5   
            
            record.peso_neto = peso_neto
            record.peso_bruto = peso_bruto
            record.peso_metro = peso_metro
    
    """
    
    @api.multi
    def _get_valores(self):
        for record in self:
            cambios_fabricacion = False
        
            if record.user_cantonera_color_id:
                record.cantonera_color_id = record.user_cantonera_color_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            if record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.cantonera_color_id:
                    record.cantonera_color_id = record.sale_order_line_id.oferta_id.attribute_id.cantonera_color_id.id
            
            if record.user_cantonera_forma_id:
                record.cantonera_forma_id = record.user_cantonera_forma_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.cantonera_forma_id:
                    record.cantonera_color_id = record.sale_order_line_id.oferta_id.attribute_id.cantonera_forma_id.id
            
            if record.user_cantonera_especial_id:
                record.cantonera_especial_id = record.user_cantonera_especial_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.cantonera_especial_id:
                    record.cantonera_especial_id = record.sale_order_line_id.oferta_id.attribute_id.cantonera_especial_id.id
            
            if record.user_cantonera_impresion_id:
                record.cantonera_impresion_id = record.user_cantonera_impresion_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.cantonera_impresion_id:
                    record.cantonera_impresion_id = record.sale_order_line_id.oferta_id.attribute_id.cantonera_impresion_id.id
            
            if record.user_cantonera_cliche_id:
                record.cantonera_cliche_id = record.user_cantonera_cliche_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.cantonera_cliche_id:
                    record.cantonera_cliche_id = record.sale_order_line_id.oferta_id.attribute_id.cantonera_cliche_id.id
            
            if record.user_fsc_id:
                record.fsc_id = record.user_fsc_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.fsc_id:
                    record.fsc_id = record.sale_order_line_id.oferta_id.attribute_id.fsc_id.id
            
            if record.user_reciclable_id:
                record.reciclable_id = record.user_reciclable_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.reciclable_id:
                    record.reciclable_id = record.sale_order_line_id.oferta_id.attribute_id.reciclable_id.id
            
            if record.user_perfilu_color_id:
                record.perfilu_color_id = record.user_perfilu_color_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.perfilu_color_id:
                    record.perfilu_color_id = record.sale_order_line_id.oferta_id.attribute_id.perfilu_color_id.id
            
            if record.user_inglete_id:
                record.inglete_id = record.user_inglete_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.inglete_id:
                    record.inglete_id = record.sale_order_line_id.oferta_id.attribute_id.inglete_id.id
            
            if record.user_inglete_num > 0:
                record.inglete_num = record.user_inglete_num
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.inglete_num > 0:
                    record.inglete_num = record.sale_order_line_id.oferta_id.attribute_id.inglete_num
            
            if record.user_inglete_texto:
                record.inglete_texto = record.user_inglete_texto
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.inglete_texto:
                    record.inglete_texto = record.sale_order_line_id.oferta_id.attribute_id.inglete_texto
                    
            if record.user_plancha_color_id:
                record.plancha_color_id = record.user_plancha_color_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.plancha_color_id:
                    record.plancha_color_id = record.sale_order_line_id.oferta_id.attribute_id.plancha_color_id.id
            
            if record.user_papel_calidad_id:
                record.papel_calidad_id = record.user_papel_calidad_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.papel_calidad_id:
                    record.papel_calidad_id = record.sale_order_line_id.oferta_id.attribute_id.papel_calidad_id.id
            
            if record.user_troquelado_id:
                record.troquelado_id = record.user_troquelado_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.troquelado_id:
                    record.troquelado_id = record.sale_order_line_id.oferta_id.attribute_id.troquelado_id.id
                    
            if record.user_paletizado:
                if record.user_paletizado == '1':
                    record.paletizado = 1
                elif record.user_paletizado == '2':
                    record.paletizado = 2
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.paletizado > 0:
                    record.paletizado = record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.paletizado
                    
            if record.user_pallet_especial_id:
                record.pallet_especial_id = record.user_pallet_especial_id.id
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.pallet_especial_id:
                    record.pallet_especial_id = record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.pallet_especial_id.id

            if record.user_ancho_pallet:
                if record.user_ancho_pallet == '1200':
                    record.ancho_pallet = 1200
                elif record.user_ancho_pallet == '1150':
                    record.ancho_pallet = 1150
                elif record.user_ancho_pallet == '1000':
                    record.ancho_pallet = 1000
                elif record.user_ancho_pallet == '800':
                    record.ancho_pallet = 800
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.ancho_pallet > 0:
                    record.ancho_pallet = record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.ancho_pallet
                    
            if record.user_und_paquete > 0:
                record.und_paquete = record.user_und_paquete
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.und_paquete > 0:
                    record.und_paquete = record.sale_order_line_id.oferta_id.attribute_id.referencia_cliente_id.und_paquete
                    
            if record.user_unidades > 0:
                record.unidades = record.user_unidades
                if record.sale_order_line_id:
                    cambios_fabricacion = True
            elif record.sale_order_line_id:
                if record.sale_order_line_id.und_pallet > 0:
                    record.unidades = record.sale_order_line_id.und_pallet
            
            
            record.cambios_fabricacion = cambios_fabricacion

    """

    @api.multi
    def crear_sin_pedido(self):
        for record in self:
            record._crear_referencia()
            record.product_id = record._crear_producto()

    
    
    @api.multi
    def _crear_referencia(self):
    
        if self.type_id.is_varios == True:
            
            if not self.tipo_varios_id:
                raise ValidationError("Error: Hay que indicar un valor de Varios")

            referencia_id, error = self.type_id.create_prod_varios(self.tipo_varios_id)

            if not referencia_id:
                raise ValidationError(error)

            self.referencia_id = referencia_id    
            
            
            
        if self.type_id.is_cantonera == True:

            if not self.ala_1 or self.ala_1 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ALA 1")
            if not self.ala_2 or self.ala_2 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ALA 2")
            if not self.grosor_2 or self.grosor_2 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en GROSOR")
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
                
            referencia_id, error = self.type_id.create_prod_cantonera(self.ala_1, self.ala_2, self.grosor_2, self.longitud)
            
            if not referencia_id:
                raise ValidationError(error)
 
            self.referencia_id = referencia_id    
            
            
            
        if self.type_id.is_perfilu == True:
        
            if not self.ala_1 or self.ala_1 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ALA 1")
            if not self.ancho or self.ancho <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ANCHO")
            if not self.ala_2 or self.ala_2 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ALA 2")
            if not self.grosor_2 or self.grosor_2 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en GROSOR")
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
                
            referencia_id, error = self.type_id.create_prod_perfilu(self.ala_1, self.ancho, self.ala_2, self.grosor_2, self.longitud)

            if not referencia_id:
                raise ValidationError(error)
                 
            self.referencia_id = referencia_id    
            
            
            
        if self.type_id.is_slipsheet == True:
            
            if not self.ancho or self.ancho <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ANCHO")
            if not self.grosor_1 or self.grosor_1 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en GROSOR")
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
                
            referencia_id, error = self.type_id.create_prod_slipsheet(self.ala_1, self.ancho, self.ala_2, self.grosor_1, self.longitud, self.ala_3, self.ala_4)

            if not referencia_id:
                raise ValidationError(error)
                
            self.referencia_id = referencia_id    
            
            
            
        if self.type_id.is_solidboard == True:
        
            if not self.ancho or self.ancho <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ANCHO")
            if not self.grosor_1 or self.grosor_1 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en GROSOR")
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
                
            referencia_id, error = self.type_id.create_prod_solidboard(self.ancho, self.grosor_1, self.longitud)

            if not referencia_id:
                raise ValidationError(error)
                
            self.referencia_id = referencia_id    

            
            
        if self.type_id.is_formato == True:
        
            if not self.ancho or self.ancho <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ANCHO")
            if not self.gramaje or self.gramaje <= 0:
                raise ValidationError("Error: Hay que indicar un valor en GRAMAJE")
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
                
            referencia_id, error = self.type_id.create_prod_formato(self.ancho, self.longitud, self.gramaje)

            if not referencia_id:
                raise ValidationError(error)
                
            self.referencia_id = referencia_id    
            
            
            
        if self.type_id.is_bobina == True:
        
            if not self.ancho or self.ancho <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ANCHO")
            if not self.gramaje or self.gramaje <= 0:
                raise ValidationError("Error: Hay que indicar un valor en GRAMAJE")
            if not self.diametro or self.diametro <= 0:
                raise ValidationError("Error: Hay que indicar un valor en DIÁMETRO")
                
            referencia_id, error = self.type_id.create_prod_bobina(self.ancho, self.diametro, self.gramaje)
            
            if not referencia_id:
                raise ValidationError(error)
                
            self.referencia_id = referencia_id    
            
            
            
        if self.type_id.is_pieballet == True:
        
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
            if not self.pie:
                raise ValidationError("Error: Hay que indicar un valor en PIE")
                
            referencia_id, error = self.type_id.create_prod_pieballet(self.longitud, self.pie)

            if not referencia_id:
                raise ValidationError(error)
                
            self.referencia_id = referencia_id    
            
            
            
        if self.type_id.is_flatboard == True:
        
            if not self.ancho or self.ancho <= 0:
                raise ValidationError("Error: Hay que indicar un valor en ANCHO")
            if not self.grosor_1 or self.grosor_1 <= 0:
                raise ValidationError("Error: Hay que indicar un valor en GROSOR")
            if not self.longitud or self.longitud <= 0:
                raise ValidationError("Error: Hay que indicar un valor en LONGITUD")
                
            referencia_id, error = self.type_id.create_prod_flatboard(self.ancho, self.grosor_1, self.longitud)

            if not referencia_id:
                raise ValidationError(error)
                
            self.referencia_id = referencia_id    

            
            
    @api.multi
    def _crear_producto(self):
        for record in self:
            product_id = None
            for prod in self.env['product.template'].search([('referencia_id', '=', self.referencia_id.id),
                                                             ]):
                product_id = prod
                
            if product_id == None:
                es_vendido = False
                es_comprado = False
                tipo_producto = ''
                cuenta_ingresos_code = -1
                cuenta_gastos_code = -1
                
                if record.is_cantonera == True:
                    es_vendido = True
                    es_comprado = False
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70100001
                    cuenta_gastos_code = -1
                if record.is_perfilu == True:
                    es_vendido = True
                    es_comprado = True
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000008
                    cuenta_gastos_code = 60000003
                if record.is_slipsheet == True:
                    es_vendido = True
                    es_comprado = False
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70100009
                    cuenta_gastos_code = -1
                if record.is_solidboard == True:
                    es_vendido = True
                    es_comprado = False
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000011
                    cuenta_gastos_code = -1
                if record.is_formato == True:
                    es_vendido = True
                    es_comprado = True
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000004
                    cuenta_gastos_code = 60000004
                if record.is_bobina == True:
                    es_vendido = True
                    es_comprado = True
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000004
                    cuenta_gastos_code = 60000004
                if record.is_pieballet == True:
                    es_vendido = True
                    es_comprado = True
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000002
                    cuenta_gastos_code = 60000005
                if record.is_flatboard == True:
                    es_vendido = True
                    es_comprado = True
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000005
                    cuenta_gastos_code = 60000007
                if record.is_varios == True:
                    es_vendido = True
                    es_comprado = True
                    tipo_producto = 'consu'
                    cuenta_gastos_code = -1
                    if record.tipo_varios_id:
                        cuenta_ingresos_code = record.tipo_varios_id.number
                if record.is_mprima_papel == True:
                    es_vendido = True
                    es_comprado = False
                    tipo_producto = 'product'
                    cuenta_ingresos_code = 70000004
                    cuenta_gastos_code = 60100001
                
                product_id = self.env['product.template'].create({'name': record.referencia_id.name, 
                                                                  'type': tipo_producto,
                                                                  'purchase_ok': es_comprado,
                                                                  'sale_ok': es_vendido,
                                                                  'tracking': 'serial',
                                                                  'categ_id': record.type_id.id,
                                                                  'referencia_id':record.referencia_id.id, 
                                                                  #'property_account_income_id': 
                                                                  #'property_account_expense_id': 
                                                                 })
            return product_id.product_variant_id.id,
            
    
