from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

# Create your models here.
class Habitacion(models.Model):
    TIPO=[
        ("STD", "Standard"),
        ("DLX", "Deluxe"),
        ("STE", "Suite"),
    ]
    numero       = models.PositiveIntegerField(unique=True)
    tipo         = models.CharField(max_length=3, choices=TIPO)
    precio_noche = models.DecimalField(max_digits=8, decimal_places=2)
    capacidad    = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    disponible   = models.BooleanField(default=True)

    def __str__(self):
        return f'Hab. {self.numero} ({self.get_tipo_display()})'

class Cliente(models.Model):
    nombres   = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    email     = models.EmailField(unique=True)
    telefono  = models.CharField(max_length=20)
    dni       = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f'{self.apellidos}, {self.nombres}'


class Reserva(models.Model):
    ESTADO = [
        ('RES', 'Reservada'),
        ('CAN', 'Cancelada'),
        ('FIN', 'Finalizada'),
    ]
    habitacion  = models.ForeignKey(Habitacion, on_delete=models.PROTECT)
    cliente     = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    check_in    = models.DateField()
    check_out   = models.DateField()
    estado      = models.CharField(max_length=3, choices=ESTADO, default='RES')
    creado_el   = models.DateTimeField(auto_now_add=True)

    @property
    def noches(self):
        return (self.check_out - self.check_in).days

    def calcular_total(self):
        return self.noches * self.habitacion.precio_noche

    def cancelar(self):
        self.estado = 'CAN'
        self.save()

    def __str__(self):
        return f'Reserva #{self.id} – {self.cliente}'


class Pago(models.Model):
    METODO = [
        ('EFC', 'Efectivo'),
        ('TDC', 'Tarjeta crédito'),
        ('TDB', 'Tarjeta débito'),
        ('PAY', 'PayPal'),
    ]
    reserva   = models.OneToOneField(Reserva, on_delete=models.CASCADE)
    monto     = models.DecimalField(max_digits=8, decimal_places=2)
    fecha     = models.DateTimeField(default=timezone.now)
    metodo    = models.CharField(max_length=3, choices=METODO)

    def __str__(self):
        return f'Pago {self.metodo} – ${self.monto}'