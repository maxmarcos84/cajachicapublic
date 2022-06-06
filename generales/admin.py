from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from generales.models import Empleado

class EmpleadoInLine(admin.StackedInline):
    model = Empleado
    can_deelete = False

class UserAdmin(BaseUserAdmin):
    inlines = (EmpleadoInLine,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)