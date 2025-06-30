from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservaForm, ClienteForm
from .models import Habitacion, Reserva, Cliente
from .forms import HabitacionForm
from .forms import PagoForm
from django.http import HttpResponse
from django.core import serializers
from django.contrib import messages
from django.core.serializers import deserialize
from django.http import HttpResponseRedirect


def listado_habitaciones(request):
    habitaciones = Habitacion.objects.filter(disponible=True)
    return render(request, 'hotel/listado.html', {'habitaciones': habitaciones})

def reservar(request, hab_id):
    habitacion = get_object_or_404(Habitacion, id=hab_id, disponible=True)
    form = ReservaForm(request.POST or None, initial={'habitacion': habitacion})
    total = None

    if request.method == 'POST' and form.is_valid():
        reserva = form.save(commit=False)
        noches = (reserva.check_out - reserva.check_in).days
        total = noches * habitacion.precio_noche
        reserva.total = total
        reserva.save()
        habitacion.disponible = False
        habitacion.save()
        return redirect('hotel:detalle_reserva', reserva.id)

    # Si las fechas ya están ingresadas, calculamos el total sin guardar
    elif request.method == 'POST':
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        if check_in and check_out:
            from datetime import datetime
            try:
                fecha_inicio = datetime.strptime(check_in, "%Y-%m-%d").date()
                fecha_fin = datetime.strptime(check_out, "%Y-%m-%d").date()
                noches = (fecha_fin - fecha_inicio).days
                if noches > 0:
                    total = noches * habitacion.precio_noche
            except:
                pass

    return render(request, 'hotel/reservar.html', {
        'form': form,
        'habitacion': habitacion,
        'total': total
    })

def detalle_reserva(request, res_id):
    reserva = get_object_or_404(Reserva, id=res_id)
    return render(request, 'hotel/detalle.html', {'reserva': reserva})

def cancelar_reserva(request, res_id):
    reserva = get_object_or_404(Reserva, id=res_id)
    reserva.cancelar()
    reserva.habitacion.disponible = True
    reserva.habitacion.save()
    return redirect('detalle_reserva', res_id)

def registrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hotel:listado_habitaciones')
    else:
        form = ClienteForm()
    return render(request, 'hotel/registrar_cliente.html', {'form': form})

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'hotel/lista_clientes.html', {'clientes': clientes})

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    form = ClienteForm(request.POST or None, instance=cliente)
    if form.is_valid():
        form.save()
        return redirect('hotel:lista_clientes')
    return render(request, 'hotel/editar_cliente.html', {'form': form, 'cliente': cliente})

def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('hotel:lista_clientes')
    return render(request, 'hotel/eliminar_cliente.html', {'cliente': cliente})

def registrar_habitacion(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hotel:listado_habitaciones')
    else:
        form = HabitacionForm()
    return render(request, 'hotel/registrar_habitacion.html', {'form': form})

def registrar_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hotel:listado_habitaciones')
    else:
        form = ReservaForm()
    return render(request, 'hotel/registrar_reserva.html', {'form': form})

def registrar_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hotel:listado_habitaciones')
    else:
        form = PagoForm()
    return render(request, 'hotel/registrar_pago.html', {'form': form})

def listar_reservas(request):
    reservas = Reserva.objects.all().order_by('-creado_el')
    return render(request, 'hotel/listar_reservas.html', {'reservas': reservas})

def lista_habitaciones(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'hotel/lista_habitaciones.html', {'habitaciones': habitaciones})

def editar_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    form = HabitacionForm(request.POST or None, instance=habitacion)
    if form.is_valid():
        form.save()
        return redirect('hotel:lista_habitaciones')
    return render(request, 'hotel/editar_habitacion.html', {'form': form})

def eliminar_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    habitacion.delete()
    return redirect('hotel:lista_habitaciones')

def lista_reservas(request):
    reservas = Reserva.objects.select_related('cliente', 'habitacion')
    return render(request, 'hotel/lista_reservas.html', {'reservas': reservas})

def editar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    form = ReservaForm(request.POST or None, instance=reserva)
    if form.is_valid():
        form.save()
        return redirect('hotel:lista_reservas')
    return render(request, 'hotel/editar_reserva.html', {'form': form})

def eliminar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    reserva.delete()
    return redirect('hotel:lista_reservas')

def exportar_json(request):
    data = list(Habitacion.objects.all()) + list(Reserva.objects.all())
    json_data = serializers.serialize('json', data)

    response = HttpResponse(json_data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="backup_datos.json"'
    return response

def importar_json(request):
    if request.method == 'POST' and request.FILES.get('archivo_json'):
        archivo = request.FILES['archivo_json']
        try:
            objetos = deserialize('json', archivo.read().decode('utf-8'))
            for obj in objetos:
                obj.save()
            messages.success(request, 'Datos importados correctamente.')
        except Exception as e:
            messages.error(request, f'Error al importar: {e}')
        return redirect('hotel:listado_habitaciones')

    return render(request, 'hotel/importar_json.html')

