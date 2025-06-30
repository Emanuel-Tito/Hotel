from django.urls import path
from . import views

app_name = "hotel"

urlpatterns = [
    # Página principal y listado general
    path('', views.listado_habitaciones, name='listado_habitaciones'),

    # Reservar habitación y ver detalle
    path('habitacion/<int:hab_id>/reservar/', views.reservar, name='reservar'),
    path('reserva/<int:res_id>/', views.detalle_reserva, name='detalle_reserva'),
    path('reserva/<int:res_id>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),

    # Clientes
    path('registrar-cliente/', views.registrar_cliente, name='registrar_cliente'),
    path('usuarios/', views.lista_clientes, name='lista_clientes'),
    path('usuarios/<int:cliente_id>/editar/', views.editar_cliente, name='editar_cliente'),
    path('usuarios/<int:cliente_id>/eliminar/', views.eliminar_cliente, name='eliminar_cliente'),

    # Habitaciones
    path('registrar-habitacion/', views.registrar_habitacion, name='registrar_habitacion'),
    path('habitaciones/', views.lista_habitaciones, name='lista_habitaciones'),
    path('habitaciones/<int:pk>/editar/', views.editar_habitacion, name='editar_habitacion'),
    path('habitaciones/<int:pk>/eliminar/', views.eliminar_habitacion, name='eliminar_habitacion'),

    # Reservas
    path('registrar-reserva/', views.registrar_reserva, name='registrar_reserva'),
    path('reservas/', views.lista_reservas, name='lista_reservas'),
    path('reservas/<int:pk>/editar/', views.editar_reserva, name='editar_reserva'),
    path('reservas/<int:pk>/eliminar/', views.eliminar_reserva, name='eliminar_reserva'),

    # Pagos
    path('registrar-pago/', views.registrar_pago, name='registrar_pago'),

    # Ver todas las reservas en orden
    path('ver-reservas/', views.listar_reservas, name='listar_reservas'),
    path('exportar-json/', views.exportar_json, name='exportar_json'),
    path('importar-json/', views.importar_json, name='importar_json'),


]




