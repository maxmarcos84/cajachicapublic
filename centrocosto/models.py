from django.db import models
from django.contrib.auth.models import User
from centrocosto.managers import ComponenteBaseManager, CentroCostoManager

# Create your models here.

class ComponenteBase(models.Model):
    id = models.AutoField(primary_key = True)
    codigo = models.CharField(
        max_length =4,
        unique = True,
        default=None   
    )
    descripcion = models.CharField(max_length=30)
    activo = models.BooleanField(default=True)
    objects =ComponenteBaseManager()
    
    class Meta:
        abstract = True

class Grupo(ComponenteBase):
    def save(self):
        self.descripcion = self.descripcion.upper()
        self.codigo = self.codigo.upper()
        super(Grupo, self).save()

    def __str__(self):
        return self.descripcion
  

class Zona(ComponenteBase):
    def save(self):
        self.descripcion = self.descripcion.upper()
        self.codigo = self.codigo.upper()
        super(Zona, self).save()

    def __str__(self):
        return self.descripcion

class Proyecto(ComponenteBase):
    def save(self):
        self.descripcion = self.descripcion.upper()
        self.codigo = self.codigo.upper()
        super(Proyecto, self).save()

    def __str__(self):
        return self.descripcion

class Concepto(ComponenteBase):
    def save(self):
        self.descripcion = self.descripcion.upper()
        self.codigo = self.codigo.upper()
        super(Concepto, self).save()

    def __str__(self):
        return self.descripcion

class TipoComprobante(ComponenteBase):
    def save(self):
        self.descripcion = self.descripcion.upper()
        self.codigo = self.codigo.upper()
        super(TipoComprobante, self).save()

    def __str__(self):
        return self.descripcion

class CentroDeCosto(models.Model):
    id = models.AutoField(primary_key = True)
    codigo = models.CharField(
        max_length =20,
        unique = True,
        default=None   
    )
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)    
    objects = CentroCostoManager()
    saldo = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)