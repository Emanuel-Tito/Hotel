from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model  = Reserva
        fields = ['habitacion', 'cliente', 'check_in', 'check_out']
