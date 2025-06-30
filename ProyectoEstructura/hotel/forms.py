from django import forms
from .models import Reserva, Cliente, Habitacion, Pago
from django.core.exceptions import ValidationError
from datetime import date

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombres', 'apellidos', 'email', 'telefono', 'dni']

    def clean_nombres(self):
        nombres = self.cleaned_data.get('nombres', '')
        if not nombres.replace(" ", "").isalpha():
            raise forms.ValidationError("Solo se permiten letras en el nombre.")
        return nombres

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos', '')
        if not apellidos.replace(" ", "").isalpha():
            raise forms.ValidationError("Solo se permiten letras en los apellidos.")
        return apellidos

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '')
        if not telefono.isdigit():
            raise forms.ValidationError("El número de teléfono debe contener solo números.")
        return telefono

    def clean_dni(self):
        dni = self.cleaned_data.get('dni', '')
        if not dni.isdigit():
            raise forms.ValidationError("El DNI debe contener solo números.")
        return dni


class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['numero', 'tipo', 'precio_noche', 'capacidad', 'disponible']
        labels = {
            'numero': 'Número de Habitación',
            'tipo': 'Tipo',
            'precio_noche': 'Precio por Noche',
            'capacidad': 'Capacidad',
            'disponible': '¿Disponible?',
        }


class ReservaForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), label="Cliente")

    class Meta:
        model = Reserva
        fields = ['cliente', 'habitacion', 'check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        habitacion = cleaned_data.get('habitacion')
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        hoy = date.today()

        if check_in and check_in < hoy:
            raise ValidationError("La fecha de entrada no puede ser en el pasado.")
        if check_out and check_out <= check_in:
            raise ValidationError("La fecha de salida debe ser posterior a la fecha de entrada.")

        if habitacion and check_in and check_out:
            reservas = Reserva.objects.filter(
                habitacion=habitacion,
                estado='RES',
                check_out__gt=check_in,
                check_in__lt=check_out,
            )
            if reservas.exists():
                raise ValidationError("La habitación seleccionada ya está reservada en esas fechas.")


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['reserva', 'monto', 'metodo']
        widgets = {
            'reserva': forms.Select(attrs={'class': 'form-select'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'metodo': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_reserva(self):
        reserva = self.cleaned_data.get('reserva')
        if Pago.objects.filter(reserva=reserva).exists():
            raise forms.ValidationError("Esta reserva ya tiene un pago registrado.")
        return reserva
