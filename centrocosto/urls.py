from django.urls import include, path

from centrocosto.views import *

urlpatterns=[
    path('grupos', GrupoView.as_view(), name='grupo_list'),
    path('grupo/Add', GrupoAdd.as_view(), name='grupo_add'),
    path('zona', ZonaView.as_view(), name='zona_list'),
    path('zona/Add', ZonaAdd.as_view(), name='zona_add' ),
    path('proyecto', ProyectoView.as_view(), name='proyecto_list'),
    path('proyecto/Add', ProyectoAdd.as_view(), name='proyecto_add'),
    path('concepto', ConceptoView.as_view(), name='concepto_list'),
    path('concepto/Add', ConceptoAdd.as_view(), name='concepto_add'),
    path('tipocomprobante', TipoComprobanteView.as_view(), name='tipocomprobante_list'),
    path('tipocomprobante/Add', TipoComprobanteAdd.as_view(), name='tipocomprobante_add'),
    path('centrodecosto', CentroDeCostoView.as_view(), name='centrodecosto_list'),
    path('centrodecosto/Add', CentroDeCostoAdd.as_view(), name='centrodecosto_add')
]