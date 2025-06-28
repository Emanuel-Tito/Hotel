from django.contrib import admin
from .models import Habitacion, Cliente, Reserva, Pago
# Register your models here.

admin.site.register(Habitacion)
admin.site.register(Cliente)
admin.site.register(Reserva)
admin.site.register(Pago)