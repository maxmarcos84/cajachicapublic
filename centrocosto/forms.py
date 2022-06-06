from django import forms

from centrocosto.models import CentroDeCosto, Grupo, Zona, Proyecto, Concepto, TipoComprobante

class GrupoForm(forms.ModelForm):
    class Meta:
        model=Grupo
        fields = ['codigo', 'descripcion', 'activo']
        labels = {'codigo' : "Codigo de grupo",
                    'descripcion' : "Descripcion del grupo",
                    'activo': "Estado"}
        widget = {'codigo' : forms.TextInput(), 'decripcion' : forms.TextInput()}

    ## En este init recorremos todos los campos y le asignamos la clase 'form-control'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'form-control'
            })

class ZonaForm(forms.ModelForm):
    class Meta:
        model=Zona
        fields = ['codigo', 'descripcion', 'activo']
        labels = {'codigo' : "Codigo de grupo",
                    'descripcion' : "Descripcion de la Zona",
                    'activo': "Estado"}
        widget = {'codigo' : forms.TextInput(), 'decripcion' : forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'form-control'
            })

class ProyectoForm(forms.ModelForm):
    class Meta:
        model=Proyecto
        fields = ['codigo', 'descripcion', 'activo']
        labels = {'codigo' : "Codigo de grupo",
                    'descripcion' : "Descripcion del Proyecto",
                    'activo': "Estado"}
        widget = {'codigo' : forms.TextInput(), 'decripcion' : forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'form-control'
            })


class ConceptoForm(forms.ModelForm):
    class Meta:
        model=Concepto
        fields = ['codigo', 'descripcion', 'activo']
        labels = {'codigo' : "Codigo de concepto",
                    'descripcion' : "Descripcion del Concepto",
                    'activo': "Estado"}
        widget = {'codigo' : forms.TextInput(), 'decripcion' : forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'form-control'
            })

class TipoComprobanteForm(forms.ModelForm):
    class Meta:
        model=TipoComprobante
        fields = ['codigo', 'descripcion', 'activo']
        labels = {'codigo' : "Codigo de comprobante",
                    'descripcion' : "Descripcion del Comprobante",
                    'activo': "Estado"}
        widget = {'codigo' : forms.TextInput(), 'decripcion' : forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'form-control'
            })

class CentroDeCostoForm(forms.ModelForm):
    class Meta:
        model=CentroDeCosto
        fields = ['codigo', 'descripcion','activo']
        labels = {'codigo': "Codigo de Centro de Costo",
                    'descripcion': "Descripcion de Centro de Costo",
                    'activo': "Estado"}
        widget = {'codigo' : forms.TextInput(), 'decripcion' : forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class' : 'form-control'
            })