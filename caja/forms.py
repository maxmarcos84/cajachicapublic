from django import forms
from django.forms import fields

from caja.models import *
from centrocosto.models import *

from django.contrib.auth.models import User

class CajaForm(forms.ModelForm):
    usuarioCaja = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True).order_by('username')        
    )    
    class Meta:
        model=Caja
        fields = ['usuarioCaja','saldo', 'activa' ]
        labels = {
            'usuarioCaja': 'Usuario',
            'saldo':'Saldo',
            'activa': 'Estado'}
    
    def __init__(self, *args, **kwargs):        
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['usuarioCaja'].empty_label="Seleccione Usuario"
        #self.fields['saldo'].widget.attrs['readonly'] =True    
        

class RendicionForm(forms.ModelForm):

    class Meta:
        model=Rendicion
        fields =['fechaInicioSemana', 'fechaFinalSemana' ]
        labels = {'fechaInicioSemana':'Desde', 'fechaFinalSemana':'Hasta'}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fechaInicioSemana'].widget.attrs.update({
            'id':'fechaInicioSemana',
            'placeholder':'Seleccionar semana'
        })
        self.fields['fechaFinalSemana'].widget.attrs.update({
            'id':'fechaFinalSemana',
            'readonly':'True'
        })
        
class RegistroForm(forms.ModelForm):    
    ##grupo = forms.ModelChoiceField(queryset=Grupo.objects.all(), empty_label="Grupo")
    class Meta:
        model= Registro
        fields = ['descripcion', 'grupo', 'zona', 'proyecto', 'concepto', 'tipocomprobante', 'ingreso', 'egreso']
        #labels ={'fechaInicioSemana':'Fecha Algo'}
        
    def __init__(self, *args, **kwargs):        
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields["grupo"].empty_label="Grupo"
        self.fields["zona"].empty_label="Zona"
        self.fields["proyecto"].empty_label="Proyecto"
        self.fields["concepto"].empty_label="Concepto"
        self.fields["tipocomprobante"].empty_label="TipoComprobante"
        """ No voy a utilizar este campo
        self.fields["incremento"].widget.attrs.update({
            'class':'form-check-input',
            'id': 'chkincremento'
        })""" 

class CargarRendicionForm(forms.Form):      
    archivoRendicion = forms.FileField()
    
           
   
    