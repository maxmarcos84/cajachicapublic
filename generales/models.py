from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    iniciales = models.CharField(max_length=4, unique=True)

