
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

  
    
    if self.type_id.is_cantonera == True:
        mediaAlas = (self.ala_1 + self.ala_2) / 2
        und_paquete = 0
        paquetes_fila = 0
        anchoPallet = int(self.ancho_pallet_id.name)
        
        if self.und_paquete_cliente == 0 and self.longitud >= 250:

            if self.paletizado == 0:
                undFilaMax = int((anchoPallet - 0.7071 * mediaAlas) / (self.grosor / 1.5))		
                if self.grosor >= 5:
                    und_paquete = 10
                elif self.grosor >= 4:
                    und_paquete = 20
                else:
                    und_paquete = 25	
                    
                pesoPaquete = peso * self.longitud / 1000 * und_paquete
                while pesoPaquete > 20:
                    self.und_paquete = und_paquete - 5
                    pesoPaquete = peso * self.longitud / 1000 * und_paquete
                    
                self.paquetes_fila = int(undFilaMax / und_paquete)	
                
            elif self.paletizado == 1:
                if anchoPallet == 1200:
                    anchoPallet = 1150

                undColumna = int(((anchoPallet - 10) / 4 - 0.7071 * mediaAlas) / (self.grosor / 1.5))
                paquetesColumna = 2
                und_paquete = int(undColumna / paquetesColumna)
                pesoPaquete = peso * self.longitud / 1000 * und_paquete
                while pesoPaquete > 20:
                    paquetesColumna = paquetesColumna + 1
                    self.und_paquete = int(undColumna / paquetesColumna)
                    pesoPaquete = peso * self.longitud / 1000 * und_paquete
                    
                self.paquetes_fila = paquetesColumna * 4
                
        elif self.und_paquete_cliente > 0 and self.longitud >= 250:	
            self.und_paquete = self.und_paquete_cliente
            undFilaMax = int((anchoPallet - 0.7071 * mediaAlas) / (self.grosor / 1.5))
            self.paquetes_fila = int(undFilaMax / und_paquete)	
    
    
    
    
    
    
    
    
    
    
    