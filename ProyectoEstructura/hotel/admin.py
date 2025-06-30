from django.contrib import admin
from .models import Habitacion, Cliente, Reserva, Pago
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as DefaultGroupAdmin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

class CustomUserAdmin(DefaultUserAdmin):
    search_fields = ['username', 'first_name', 'last_name', 'email']
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)



class GroupAdminSinPermisos(DefaultGroupAdmin):
    exclude = ('permissions',)  # Oculta el campo en el formulario

# Desregistrar el admin original y registrar el nuevo
admin.site.unregister(Group)
admin.site.register(Group, GroupAdminSinPermisos)



admin.site.register(Habitacion)
admin.site.register(Cliente)
admin.site.register(Reserva)
admin.site.register(Pago)
admin.site.site_header = "Hotel Ruby"
admin.site.site_title  = "Panel Hotel Ruby"
admin.site.index_title = "Menú de administración"