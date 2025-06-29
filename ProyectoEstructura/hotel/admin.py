from django.contrib import admin
from .models import Habitacion, Cliente, Reserva, Pago
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as DefaultGroupAdmin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

class CustomUserAdmin(DefaultUserAdmin):
    search_fields = ['username', 'first_name', 'last_name', 'email']  # campos a buscar

admin.site.unregister(User)  # desregistrar el original
admin.site.register(User, CustomUserAdmin)  # registrar el modificado


# Nueva clase que oculta el campo permissions
class GroupAdminSinPermisos(DefaultGroupAdmin):
    exclude = ('permissions',)  # Oculta el campo en el formulario

# Desregistrar el admin original y registrar el nuevo
admin.site.unregister(Group)
admin.site.register(Group, GroupAdminSinPermisos)

# Register your models here.

admin.site.register(Habitacion)
admin.site.register(Cliente)
admin.site.register(Reserva)
admin.site.register(Pago)
admin.site.site_header = "Hotel Ruby"
admin.site.site_title  = "Panel Hotel Ruby"
admin.site.index_title = "Menú de administración"