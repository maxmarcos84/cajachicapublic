from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import *
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic

from centrocosto.models import CentroDeCosto
from caja.models import *

from datetime import date, datetime
import calendar, locale
##locale.setlocale(locale.LC_ALL, 'es-ES')

# Create your views here.

class SinPrivilegios(PermissionRequiredMixin):
    login_url='generales:sin_privilegios'
    raise_exception = False
    redirect_field_name="redirecto_to"

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy(self.login_url))

class Home(LoginRequiredMixin, View):
    template_name='generales/home.html'
    login_url='generales:login'

    class Caja_mostrar:
        usuario = models.CharField()
        saldo = models.IntegerField()

    class Dias_retraso:
        usuario = models.CharField()
        dias = models.IntegerField()

    class CentroGasto:
        codigo_centro = models.CharField()
        saldo = models.IntegerField()

    class DiferenciaMensual:
        mes = models.CharField()
        incremento = models.IntegerField()
        rendido = models.IntegerField()

    def get_centros(self):
        return CentroDeCosto.objects.all()

    def get_gastos_centro(self):
        centros = CentroDeCosto.objects.filter(activo = True)
        lista = list()
        for centro in centros:
            nuevo_centro = self.CentroGasto()
            nuevo_centro.codigo_centro = centro.codigo
            #nuevo_centro.saldo = Registro.objects.get_centroCosto_saldo_ultimoMes(centro)
            nuevo_centro.saldo = Registro.objects.get_centroCosto_saldo_ultimoAño(centro)
            lista.append(nuevo_centro)
        return lista

    def get_cajas(self):
        cajas = Caja.objects.filter(activa = True)        
        lista = list()
        for caja in cajas:
            caja_mostrar = self.Caja_mostrar()
            nombre_usuario = caja.usuarioCaja.first_name +" "+ caja.usuarioCaja.last_name
            caja_mostrar.usuario = nombre_usuario            
            caja_mostrar.saldo = int(float(caja.saldo))
            lista.append(caja_mostrar)
        return lista

    def get_dias_retraso(self):
        cajas = Caja.objects.filter(activa = True)
        rendiciones = Rendicion.objects.get_ultimas_rendiciones_porcaja(cajas)
        lista = list()
        totalRendiciones = rendiciones.count(id)
        if len(rendiciones) > 0:
            for rend in rendiciones:
                dias_retraso = self.Dias_retraso()
                dias_retraso.usuario = rend.Caja.usuarioCaja.first_name +" "+ rend.Caja.usuarioCaja.last_name
                fecha_ultimo_registro = rend.fecha
                fecha_actual = datetime.today()
                dias_retraso.dias = (fecha_actual.replace(tzinfo=None)  - fecha_ultimo_registro.replace(tzinfo=None) ).days
                if dias_retraso.dias < 1:
                    dias_retraso.dias = 1
                lista.append(dias_retraso)
        return lista

    def get_diferencia_mensual(self):
        lista = list()
        ano = datetime.now().year
        for x in range(1, 13):
            diferencia = self.DiferenciaMensual()
            diferencia.mes = calendar.month_name[x]
            diferencia.incremento = int(float(Registro.objects.get_incrementos_mes(ano, x))) 
            diferencia.rendido = int(float(Registro.objects.get_egresos_mes(ano, x))) 
            lista.append(diferencia)
        return lista


    def get(self, request, *args, **kwargs):
        centros = self.get_gastos_centro()
        saldos = [int(float(x.saldo)) for x in centros]
        cajas = self.get_cajas()
        dias_retraso = self.get_dias_retraso()
        gastos_centros = self.get_gastos_centro()
        diferencia_mensual = self.get_diferencia_mensual()
        contexto = {'centros': centros,
                    'saldos' : saldos,
                    'cajas': cajas,
                    'dias_retraso': dias_retraso,
                    'diferencia_mensual': diferencia_mensual }        
        return render(request, self.template_name, contexto)

class HomeSinPrivilegios(generic.TemplateView):
    template_name='generales/sin_privilegios.html'