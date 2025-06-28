from django.urls import path
from . import views

app_name = "hotel"

urlpatterns = [
    path('', views.listado_habitaciones, name='listado_habitaciones'),
    path('habitacion/<int:hab_id>/reservar/', views.reservar, name='reservar'),
    path('reserva/<int:res_id>/', views.detalle_reserva, name='detalle_reserva'),
    path('reserva/<int:res_id>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),
]
