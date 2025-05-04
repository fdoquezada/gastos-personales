from django.db import models
from django.utils import timezone

class Transaccion(models.Model):
    TIPO_CHOICES = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    )
    fecha = models.DateField(default=timezone.now)
    descripcion = models.CharField(max_length=200)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    mes = models.DateField()  # Para agrupar por mes

    def __str__(self):
        return f'{self.fecha} - {self.descripcion} ({self.tipo})'

    class Meta:
        ordering = ['-fecha']
# Create your models here.
