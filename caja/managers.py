#from caja.models import Caja, Rendicion, Registro
from centrocosto.models import *
from django.db import models 
from generales.models import Empleado
from caja.models import *
from decimal import Decimal
from datetime import datetime

class RendicionManager(models.Manager):

    def get_rendiciones(self, caja_id):
        return self.filter(Caja = caja_id).order_by('-id')[:4]
        #esta en caso de armar una pagina para que cada usuario pueda ver sus rendiciones
        #o para cuando implemente un usuario aprobador de rendiciones.

    def get_ultimas_rendiciones(self):
        return self.all().order_by('-id')[:4]
        

    def get_caja_abierta(self, caja_id):
        return self.filter(Caja = caja_id).filter(cerrada = False).exists()

    def actualizar_montos(self, rendicion , incremento, egreso, saldoCaja):        
        rendicion.totalIncremento = Decimal(incremento)
        rendicion.totalEgreso = Decimal(egreso)
        rendicion.totalRendicion += (Decimal(incremento) - Decimal(egreso))
        rendicion.saldoCaja = Decimal(saldoCaja)
        rendicion.save()
        
    ##Debo obtener mucha madera
    def get_ultimas_rendiciones_porcaja(self, cajas):
        ##cajas = Caja.objects.filter(activa = True)
        lista_rendiciones = list()
        for caj in cajas:
            rendicion = self.filter(Caja = caj).last()
            if(rendicion):
                lista_rendiciones.append(rendicion)
        return lista_rendiciones  


class RegistroManager(models.Manager):
    def get_centroCosto_saldo_ultimoMes(self, centroCosto):
        saldo = Decimal()        
        registros = self.filter(centrodecosto = centroCosto, 
                                fecha__year = datetime.now().year,
                                fecha__month = datetime.now().month)                                
        for reg in registros:
            saldo += reg.egreso
        return saldo

    def get_centroCosto_saldo_ultimoAño(self, centroCosto):
        saldo = Decimal()        
        registros = self.filter(centrodecosto = centroCosto,
                                fecha__year = datetime.now().year, anulado = False)
        for reg in registros:
            saldo +=reg.egreso
        return saldo

    def get_incrementos_mes(self, ano, mes):
        totalInc = Decimal()        
        incrementos = self.filter(incremento = True,
                                  fecha__year = ano,
                                  fecha__month = mes )
        for reg in incrementos:
            totalInc += reg.ingreso
        return totalInc

    def get_egresos_mes(self, ano, mes):
        totalEgr = Decimal()
        egresos = self.filter(incremento = False,
                              fecha__year = ano,
                              fecha__month = mes )
        for reg in egresos:
            totalEgr += reg.egreso
        return totalEgr
        

class CajaManager(models.Manager):
    def get_caja_byUser(self, usuario):        
        #empleado = Empleado.objects.filter(iniciales = iniciales_empleado).first()
        #usuario = empleado.user}
        try:
            caja = self.filter(usuarioCaja = usuario).filter(activa = True).first()
            return caja   
        except Exception as e:
            e.error = "El usuario no tiene caja"
            return e

    def actualizar_saldo_caja(self, caja_id, ingreso, egreso):
        caja_actual = self.filter(id = caja_id).first()
        saldo_actual = Decimal(caja_actual.saldo)
        saldo_nuevo = saldo_actual +(Decimal(ingreso) - Decimal(egreso))
        caja_actual.saldo = saldo_nuevo
        caja_actual.save()
        return saldo_nuevo        

    def get_user_by_iniciales(self, iniciales):
        empleado = Empleado.objects.filter(iniciales = iniciales).first()
        return empleado

