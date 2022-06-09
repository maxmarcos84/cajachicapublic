from django.db.models.base import Model
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import *
from django.urls import reverse_lazy 
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import ValidationError
from datetime import date, datetime
from decimal import Decimal
from django.core import serializers
from django.contrib.messages.views import SuccessMessageMixin

import pandas as pd
import json

from .managers import *
from .models import Caja, Rendicion, Registro
from .forms import CajaForm, RegistroForm, RendicionForm, CargarRendicionForm
from generales.views import SinPrivilegios

from centrocosto.models import *

class CajaListaView(LoginRequiredMixin, ListView):
    model = Caja
    template_name ="caja/caja_list.html"
    context_object_name = "obj"
    login_url='generales:login'
    queryset = Caja.objects.filter(activa = True) #esto filtra mas sencillo
   

class CajaAddView(LoginRequiredMixin, SinPrivilegios, CreateView):
    permission_required = "caja.add_caja"
    model = Caja
    template_name = "caja/caja_add.html"
    context_object_name ="obj"
    form_class= CajaForm
    success_url = reverse_lazy("caja:caja_list")

    def post(self, request, *args, **kwargs):
        form= CajaForm(request.POST or None, request.FILES or None)
        if form.is_valid():            
            if Caja.objects.filter(usuarioCaja = request.POST['usuarioCaja'], activa = True).exists():                
                ##raise ValidationError(u'Ya exite una caja abierta asignada a este usuario')
                messages.error(request, 'Ya exite una caja abierta asignada a este usuario')                
                return render(request, "caja/caja_add.html",context={"form": form,})
            else:
                instance = form.save(commit=False)
                instance.usuarioCreador = request.user
                instance.save()
                context ={"form": form,}
                cajas = Caja.objects.all()
                return render(request, "caja/caja_list.html",{'obj':cajas})

class CajaRegistroRendicion(LoginRequiredMixin, View):
    model = Registro
    template_name = "caja/registro_rendicion.html"
    form_class = RegistroForm
    success_url = reverse_lazy("caja:caja_registro_rendicion")
    context = {"formRegistro": form_class,}

    def get(self, request, *args, **kwargs):                
        return render(request, self.template_name, self.context)

class CajaRendirView(LoginRequiredMixin, View):
    model = Rendicion
    template_name ="caja/rendir_caja.html"
    form_class = RendicionForm    
    
    def get_caja(self):
        cajaRendicion = Caja.objects.filter(usuarioCaja = self.request.user).filter(activa = True)
        return cajaRendicion
 
    def get_caja_abierta(self):
        cajarendicion = self.get_caja().first()        
        return self.model.objects.get_caja_abierta(cajarendicion)

    def get_queryset(self):        
        cajarendicion = self.get_caja().first()        
        return self.model.objects.get_rendiciones(cajarendicion)
       
        #return self.model.objects.filter(Caja = cajarendicion).filter(fechaInicioSemana__month = fecha.month)
        # esto sirve para mostrar los registros del ultimo mes   

    def get_context_data(self, **kwargs):        
        contexto = {}
        contexto['form'] = self.form_class
        contexto['listado'] = self.get_queryset()
        contexto['cajaAbierta'] = self.get_caja_abierta()
        return contexto

    def get(self, request, *args, **kwargs):                
        return render(request, self.template_name, self.get_context_data())

    #definir el metodo post para que se guarde lo que ponemos en el formulario
    def post(self, request, *args, **kwargs):
        listado = self.get_context_data()
        form = RendicionForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.Caja = self.get_caja().first()
            instance.save()
            return redirect('caja:caja_registro_rendicion')
        else:
            messages.error(request, form.errors.as_data())                
            return render(request, "caja/rendir_caja.html", self.get_context_data())

class CargarRendicion(LoginRequiredMixin, SinPrivilegios, View):
    permission_required="caja.add_rendicion"
    model = Registro
    template_name = "caja/cargar_rendicion.html"
    success_url = reverse_lazy("caja:caja_rendir")
    form_class = CargarRendicionForm
    contextos ={ 'form': form_class()} 
    cargado = False

    def get_queryset(self):                       
        return Rendicion.objects.get_ultimas_rendiciones()

    def get(self, request, idRendicion, *args, **kwargs):
        if(idRendicion != 0):
            rendicionCargada = True
        else:
            rendicionCargada = False

        contexto = {'form': self.form_class(), 
        'rendicionCargada': rendicionCargada,
        'listado': self.get_queryset(),        
        }        
        return render(request, self.template_name, contexto)             

    def post(self, request, *args, **kwargs):  
        try:              
            form = CargarRendicionForm(request.POST, request.FILES)
            if not (form.is_valid()):
                messages.error('Por favor seleccione un archivo para cargar.')
            else:
                imp_file = request.FILES["archivoRendicion"]    
                xls = pd.ExcelFile(imp_file)
                #obtener los datos del usuario y da la fecha
                dfDatos = xls.parse(
                    sheet_name="CCH", usecols=[1,2,3,4,6,7,8,9,10,11,12], header=None
                )
                iniciales = dfDatos.loc[2][12]            
                fechaDesde = dfDatos.loc[0][10]
                fechaHasta = dfDatos.loc[0][12]
                #obtener datos de caja y usuario
                empleado = Caja.objects.get_user_by_iniciales(iniciales)
                if empleado != None:
                    caja_usuario = Caja.objects.get_caja_byUser(empleado.user)
                    if caja_usuario != None:
                        saldo_caja = caja_usuario.saldo
                    else:
                        form.add_error(None, "El empleado no tiene una caja activa")
                        return render(request, "caja/cargar_rendicion.html", {'form': form} )
                else:
                    form.add_error(None, "El empleado no esta cargado en el sistema")
                    return render(request, "caja/cargar_rendicion.html", {'form': form} )                
                
                #genero rendicion pero no la guardo, la paso como variable de sesion
                rendicion_nueva = Rendicion()
                rendicion_nueva.Caja = caja_usuario
                rendicion_nueva.fechaInicioSemana = fechaDesde
                rendicion_nueva.fechaFinalSemana = fechaHasta
                rendicion_nueva.fecha = datetime.now()

                df = xls.parse(
                    sheet_name="CCH", usecols=[1,2,3,4,6,7,8,9,10,11],
                    skiprows=[0,1,2,3], nrows=31,
                    converters={'NUMERO':str}
                    )
                df.fillna('False', inplace = True)
                #Le pongo texto a las celdas vacias porque es la unica manera que encontre de filtrarlas en la busqueda
                #para que no me las muestre en pantalla
                df2 = pd.DataFrame(columns=['descripcion', 'grupo', 'zona', 'proyecto', 
                                    'concepto','fecha','numero','tipo','ingreso','egreso'])
                for index, row in df.iterrows():
                    i= int(index)    
                    if (row[0] != 'False'):
                        descripcion = row[0]
                        grupo = row[1]
                        zona = row[2]
                        proyecto = row[3]
                        concepto = row[4]
                        fecha = str(row[5]).split('T',1)[0] #json convierte las fechas con un formato rarisimo asi que elimino una parte
                        numero = str(row[6])
                        tipo = row[7]
                        if (row[8] == 'False'):
                            ingreso = "0.00"
                        else:
                            ingreso = row[8]
                        if(row[9] == 'False'):
                            egreso = "0.00"
                        else:
                            egreso = row[9]            
                        df2.loc[i] = [descripcion, grupo, zona, proyecto, concepto, fecha.split(' ')[0], str(numero), tipo, ingreso, egreso]
                        #tengo que volver a hacer un split de la fecha para que elimine los datos horarios
                
                #Pasar el dataframe a json fue la unica forma que encontre para pasar los datos al template sin que se 
                #rompiera todo
                json_records = df2.reset_index().to_json(orient ='records')
                data = []
                data = json.loads(json_records)            
                
                context_modal = { 
                    'iniciales': iniciales,
                    'fechaDesde': str(fechaDesde),
                    'fechaHasta': str(fechaHasta),
                    'saldo': str(saldo_caja),                    
                    'empleado': empleado.id
                    }
                
                #No puedo pasar un modelo por variable de sesion, solo lo paso si esta serializado como json
                rendicion_json = serializers.serialize("json", [rendicion_nueva])

                request.session['registros'] = data #guardo los registros en variable de sesion porque tengo los huevos bien puestos      
                request.session['rendicion'] = rendicion_json
                request.session['contexto'] = context_modal

            #return render(request, "caja/cargar_rendicion.html", context)
            return redirect('caja:caja_confirmar_rendicion_modal')
        except Exception as e:
            error = str(e)
            contexto = {'form': self.form_class(),                         
                        'listado': self.get_queryset(),
                        'error' : error,      
                        }
            return redirect(request, "caja/cargar_rendicion.html", contexto)

class ConfirmarRendicionModal(LoginRequiredMixin, View):
    model = Registro
    template_name = "caja/confirmar_rendicion.html"

    def get(self, request, *args, **kwargs):
        data = request.session['registros']
        rendicion_nueva = next(serializers.deserialize("json", request.session['rendicion'])).object 
        context = request.session['contexto']
        contexto = {
            'iniciales': context['iniciales'],
            'fechaDesde': datetime.strptime(context['fechaDesde'], '%Y-%m-%d %H:%M:%S'),
            'fechaHasta': datetime.strptime(context['fechaHasta'], '%Y-%m-%d %H:%M:%S'),
            'saldo': context['saldo'],                    
            'empleado': Empleado.objects.get(user = rendicion_nueva.Caja.usuarioCaja),
            'tabla': data,
        }
        return render(request, self.template_name, contexto)
    
    def post(self, request, *args, **kwargs):
        data = request.session['registros']
        rendicion_nueva = next(serializers.deserialize("json", request.session['rendicion'])).object 
        rendicion_nueva.save()   

        totalIncremento = Decimal(0.00)
        totalEgreso = Decimal(0.00)
        saldoFinalCaja = Decimal(0.00)

        for reg in data:
            registro = Registro()
            registro.descripcion = reg['descripcion']
            registro.grupo = Grupo.objects.get_by_codigo(reg['grupo'])            
            registro.zona =  Zona.objects.get_by_codigo(reg['zona'])            
            registro.proyecto = Proyecto.objects.get_by_codigo(reg['proyecto'])            
            registro.concepto = Concepto.objects.get_by_codigo(reg['concepto'])
            registro.fecha = reg['fecha']
            registro.numero = str(reg['numero'])
            registro.tipocomprobante = TipoComprobante.objects.get_by_codigo(reg['tipo'])
            registro.ingreso = Decimal(reg['ingreso'])
            registro.incremento = (registro.ingreso > 0.00) #funciona?                
            registro.egreso = Decimal(reg['egreso'])
            registro.saldo = Caja.objects.actualizar_saldo_caja(rendicion_nueva.Caja.id, registro.ingreso, registro.egreso)
            registro.rendicion = rendicion_nueva
            #obtener centro de costo
            combinacion = str(reg['grupo']) +"-"+ str(reg['zona']) +"-"+ str(reg['proyecto'])
            registro.centrodecosto = CentroDeCosto.objects.get_centrocosto(combinacion) ####probar
            registro.save()
            if(registro.centrodecosto != None):
                CentroDeCosto.objects.actualizar_saldo_centrodecosto(registro.centrodecosto.id, Decimal(reg['egreso']))
            totalIncremento += Decimal(reg['ingreso'])
            totalEgreso += Decimal(reg['egreso'])
            saldoFinalCaja = registro.saldo
        Rendicion.objects.actualizar_montos(rendicion_nueva, totalIncremento, totalEgreso, saldoFinalCaja)

        return redirect('caja:caja_cargar_rendicion')

class DetalleRendicion(LoginRequiredMixin, View):
    model = Registro
    template_name = "caja/detalle_rendicion.html"

    def get_queryset(self, idRendicion):
        return self.model.objects.filter(rendicion = idRendicion)    
        
    #en el get obtengo el parametro enviado por url
    def get(self, request, idRendicion,  *args, **kwargs):
        rendicion = Rendicion.objects.get(id = idRendicion)
        empleado = Empleado.objects.get(user = rendicion.Caja.usuarioCaja)
        contexto = {'listado': self.get_queryset(idRendicion),
                    'empleado': empleado,
                    'fechaDesde': rendicion.fechaInicioSemana,
                    'fechaHasta': rendicion.fechaFinalSemana,
                    'saldo': rendicion.Caja.saldo}
        return render(request, self.template_name, contexto)    

class AnularRegistroView(LoginRequiredMixin,  View):
    model = Registro
    template_name="caja/anular_registro_modal.html"
    
    def get(self, request, idRegistro,  *args, **kwargs):
        context = {'registro': Registro.objects.get(id = idRegistro)}
        return render(request, self.template_name, context)

    def post(self, request, idRegistro, *args, **kwargs):
        registro = Registro.objects.get(id=idRegistro)
        if request.is_ajax():
            registro.anular()
            """
            registro.anulado = True    
            rendicion = registro.rendicion            
            if (registro.incremento):
                rendicion.saldoCaja -= registro.ingreso
                rendicion.Caja.saldo -=registro.ingreso
                rendicion.Caja.save()
                rendicion.totalRendicion -= registro.ingreso
                rendicion.totalIncremento -= registro.ingreso        
            else:
                rendicion.saldoCaja += registro.egreso
                rendicion.Caja.saldo += registro.egreso
                rendicion.Caja.save()
                rendicion.totalRendicion += registro.egreso
                rendicion.totalEgreso -= registro.egreso
                registro.centrodecosto.saldo -= registro.egreso
                registro.centrodecosto.save()
            registro.save()
            rendicion.save()               
            """            
        return redirect('caja:caja_detalle_rendicion', idRendicion=registro.rendicion.id)