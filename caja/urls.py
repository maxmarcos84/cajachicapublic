from django.urls import include, path

from caja.views import *

urlpatterns=[
    path('caja', CajaListaView.as_view(), name='caja_list'),
    path('caja/Add', CajaAddView.as_view(), name='caja_add'),
    path('caja/rendicion', CajaRendirView.as_view(), name='caja_rendir'),
    path('caja/registro_rendicion', CajaRegistroRendicion.as_view(), name='caja_registro_rendicion'),
    path('caja/cargar_rendicion', CargarRendicion.as_view(), name='caja_cargar_rendicion'),
    path('caja/cargar_rendicion/<int:idRendicion>', CargarRendicion.as_view(), name='caja_cargar_rendicion'),
    path('caja/confirmar_rendicion_modal', ConfirmarRendicionModal.as_view(), name='caja_confirmar_rendicion_modal'),
    path('caja/detalle_rendicion/<int:idRendicion>', DetalleRendicion.as_view(), name='caja_detalle_rendicion'),
    path('caja/detalle_rendicion_anular_modal/<int:idRegistro>', AnularRegistroView.as_view(), name='anular_registro_modal')    
]