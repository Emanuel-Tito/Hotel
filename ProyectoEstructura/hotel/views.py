from django.shortcuts import render, redirect, get_object_or_404
from .models import Habitacion, Reserva
from .forms import ReservaForm

def listado_habitaciones(request):
    habitaciones = Habitacion.objects.filter(disponible=True)
    return render(request, 'hotel/listado.html', {'habitaciones': habitaciones})

def reservar(request, hab_id):
    habitacion = get_object_or_404(Habitacion, id=hab_id, disponible=True)
    form = ReservaForm(request.POST or None, initial={'habitacion': habitacion})
    if form.is_valid():
        reserva = form.save()
        habitacion.disponible = False
        habitacion.save()
        return redirect('detalle_reserva', reserva.id)
    return render(request, 'hotel/reservar.html', {'form': form, 'habitacion': habitacion})

def detalle_reserva(request, res_id):
    reserva = get_object_or_404(Reserva, id=res_id)
    return render(request, 'hotel/detalle.html', {'reserva': reserva})

def cancelar_reserva(request, res_id):
    reserva = get_object_or_404(Reserva, id=res_id)
    reserva.cancelar()
    reserva.habitacion.disponible = True
    reserva.habitacion.save()
    return redirect('detalle_reserva', res_id)

