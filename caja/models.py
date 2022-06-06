#from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from centrocosto.models import * 
from caja.managers import RendicionManager, RegistroManager, CajaManager

# Create your models here.

class Caja(models.Model):
    id = models.AutoField(primary_key = True)
    usuarioCaja = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuarioCaja') 
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    usuarioCreador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='usurioCreador', null=True)
    saldo = models.DecimalField(max_digits=8, decimal_places=2,default=0.00)
    activa = models.BooleanField(default=True)
    objects = CajaManager()    

class Rendicion(models.Model):
    id = models.AutoField(primary_key=True)
    Caja = models.ForeignKey(Caja, on_delete=models.CASCADE, related_name='rendicionCaja')
    fecha = models.DateTimeField(auto_now_add=True)
    fechaInicioSemana = models.DateTimeField()
    fechaFinalSemana = models.DateTimeField()
    aprobada = models.BooleanField(default=False)
    anulada = models.BooleanField(default=False)
    cerrada = models.BooleanField(default=False)
    totalIncremento = models.DecimalField(max_digits=8, decimal_places=2,default=0.00)
    totalEgreso = models.DecimalField(max_digits=8, decimal_places=2,default=0.00)
    totalRendicion = models.DecimalField(max_digits=8, decimal_places=2,default=0.00)
    saldoCaja = models.DecimalField(max_digits=8, decimal_places=2,default=0.00)
    objects = RendicionManager()


class Registro(models.Model):
    id = models.AutoField(primary_key = True)
    #caja = models.ForeignKey(Caja, on_delete=models.CASCADE, related_name='registrosCaja')
    rendicion = models.ForeignKey(Rendicion, on_delete=models.CASCADE, related_name='registroRendicion')
    incremento = models.BooleanField(default=False, null=True)
    descripcion = models.CharField(max_length=100)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, null=True, blank=True, related_name='gruposCaja')
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, null=True, blank=True, related_name='zonaCaja')
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=True, blank=True, related_name='proyectoCaja')
    concepto = models.ForeignKey(Concepto, on_delete=models.CASCADE, null=True, blank=True, related_name='conceptoCaja')
    fecha = models.DateTimeField(auto_now_add=False)
    numero = models.CharField(null=True, max_length=20)    
    tipocomprobante = models.ForeignKey(TipoComprobante, on_delete=models.CASCADE, null=True, blank=True, related_name='tipoCompCaja')
    ingreso = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    egreso = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    saldo = models.DecimalField (max_digits=8, decimal_places=2, default=0.00)    
    centrodecosto = models.ForeignKey(CentroDeCosto, on_delete=models.CASCADE, null=True, blank=True, related_name='centrodecostoCaja')
    anulado = models.BooleanField(default=False)
    objects = RegistroManager()





    
