from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy 
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.
from centrocosto.models import Grupo, Zona, Proyecto, Concepto, TipoComprobante, CentroDeCosto
from centrocosto.forms import GrupoForm, ZonaForm, ProyectoForm, ConceptoForm, TipoComprobanteForm, CentroDeCostoForm
from generales.views import SinPrivilegios

class GrupoView(LoginRequiredMixin, generic.ListView):
    
    model = Grupo
    template_name ="centrocosto/categoria_list.html"
    context_object_name = "obj"
    login_url='generales:login'

class GrupoAdd(LoginRequiredMixin, SinPrivilegios, generic.CreateView):
    permission_required ="centrocosto.add_grupo"
    model=Grupo
    template_name="centrocosto/grupo_add.html"
    context_object_name = 'obj'
    form_class = GrupoForm
    success_url = reverse_lazy("centrocosto:grupo_list")

class ZonaView(LoginRequiredMixin, generic.ListView):
    model = Zona
    template_name ="centrocosto/zona_list.html"
    context_object_name = "obj"
    login_url='generales:login'


class ZonaAdd(LoginRequiredMixin, SinPrivilegios, generic.CreateView):
    permission_required ="centrocosto.add_zona"
    model=Zona
    template_name="centrocosto/zona_add.html"
    context_object_name = 'obj'
    form_class = ZonaForm
    success_url = reverse_lazy("centrocosto:zona_list")

class ProyectoView(LoginRequiredMixin, generic.ListView):
    model = Proyecto
    template_name ="centrocosto/proyecto_list.html"
    context_object_name = "obj"
    login_url='generales:login'

class ProyectoAdd(LoginRequiredMixin, SinPrivilegios, generic.CreateView):
    permission_required ="centrocosto.add_proyecto"
    model = Proyecto
    template_name ="centrocosto/proyecto_add.html"
    context_object_name ="obj"
    form_class = ProyectoForm
    success_url = reverse_lazy("centrocosto:proyecto_list")

class ConceptoView(LoginRequiredMixin, generic.ListView):
    model = Concepto
    template_name ="centrocosto/concepto_list.html"
    context_object_name = "obj"
    login_url='generales:login'

class ConceptoAdd(LoginRequiredMixin, SinPrivilegios, generic.CreateView):
    permission_required ="centrocosto.add_concepto"
    model = Concepto
    template_name ="centrocosto/concepto_add.html"
    context_object_name ="obj"
    form_class = ConceptoForm
    success_url = reverse_lazy("centrocosto:concepto_list")

class TipoComprobanteView(LoginRequiredMixin, generic.ListView):
    model = TipoComprobante
    template_name ="centrocosto/tipocomprobante_list.html"
    context_object_name = "obj"
    login_url='generales:login'

class TipoComprobanteAdd(LoginRequiredMixin, SinPrivilegios, generic.CreateView):
    permission_required ="centrocosto.add_tipocomprobante"
    model = TipoComprobante
    template_name ="centrocosto/tipocomprobante_add.html"
    context_object_name ="obj"
    form_class = TipoComprobanteForm
    success_url = reverse_lazy("centrocosto:tipocomprobante_list")

class CentroDeCostoView(LoginRequiredMixin, generic.ListView):
    model=CentroDeCosto
    template_name="centrocosto/centrodecosto_list.html"
    context_object_name="obj"
    login_url="generales_login"

class CentroDeCostoAdd(LoginRequiredMixin, SinPrivilegios, generic.CreateView):
    permission_required ="centrocosto.add_centrodecosto"
    model = CentroDeCosto
    template_name ="centrocosto/centrodecosto_add.html"
    context_object_name = "obj"
    form_class = CentroDeCostoForm
    success_url = reverse_lazy("centrocosto:centrodecosto_list")