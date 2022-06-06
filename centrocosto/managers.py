from centrocosto.models import *
from django.db import models
from decimal import Decimal

class ComponenteBaseManager(models.Manager):
    def get_by_codigo(self,codigo_componente):
        return self.filter(codigo = codigo_componente).first()

class CentroCostoManager(models.Manager):
    def get_centrocosto(self, combinacion):
        return self.filter(codigo = combinacion).first()

    def actualizar_saldo_centrodecosto(self, id_centrocosto, monto):
        centro_costo = self.filter(id = id_centrocosto).first()
        centro_costo.saldo += Decimal(monto)
        centro_costo.save()
