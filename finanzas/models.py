from django.db import models
from django.utils import timezone
from django.db.models import Sum, F, Case, When, Value, DecimalField

class Transaccion(models.Model):
    TIPO_CHOICES = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    )
    fecha = models.DateTimeField(default=timezone.now)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    descripcion = models.CharField(max_length=200)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    mes = models.DateField()  # Para agrupar por mes
    saldo_acumulado = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.fecha} - {self.descripcion} ({self.tipo})'

    def actualizar_saldos_posteriores(self):
        """Actualiza los saldos de las transacciones posteriores"""
        from django.db import transaction
        
        with transaction.atomic():
            # Obtener transacciones posteriores ordenadas por fecha de creación
            transacciones_posteriores = Transaccion.objects.filter(
                mes=self.mes,
                fecha_creacion__gt=self.fecha_creacion
            ).order_by('fecha_creacion')
            
            saldo_actual = self.saldo_acumulado
            
            # Actualizar cada transacción posterior
            for transaccion in transacciones_posteriores:
                if transaccion.tipo == 'entrada':
                    saldo_actual += transaccion.monto
                else:
                    saldo_actual -= transaccion.monto
                
                # Actualizar solo si el saldo ha cambiado
                if transaccion.saldo_acumulado != saldo_actual:
                    Transaccion.objects.filter(pk=transaccion.pk).update(
                        saldo_acumulado=saldo_actual
                    )

    def save(self, *args, **kwargs):
        # Si es una nueva transacción o se está actualizando
        if not self.pk or 'update_fields' not in kwargs or 'saldo_acumulado' not in kwargs.get('update_fields', []):
            # Calcular el saldo acumulado basado en transacciones anteriores
            transacciones_anteriores = Transaccion.objects.filter(
                mes=self.mes,
                fecha_creacion__lte=self.fecha_creacion if self.pk else timezone.now()
            ).exclude(pk=self.pk if self.pk else None)
            
            # Calcular el saldo de transacciones anteriores
            saldo_anterior = 0
            if transacciones_anteriores.exists():
                # Obtener el saldo acumulado de la última transacción del mes anterior
                try:
                    mes_anterior = (self.mes - timezone.timedelta(days=1)).replace(day=1)
                    ultima_del_mes_anterior = Transaccion.objects.filter(mes=mes_anterior).latest('fecha_creacion')
                    saldo_anterior = ultima_del_mes_anterior.saldo_acumulado
                except Transaccion.DoesNotExist:
                    pass
                
                # Calcular el saldo acumulado hasta ahora
                saldo_actual = saldo_anterior + sum(
                    t.monto if t.tipo == 'entrada' else -t.monto 
                    for t in transacciones_anteriores
                )
                self.saldo_acumulado = saldo_actual + (self.monto if self.tipo == 'entrada' else -self.monto)
            else:
                # Es la primera transacción del mes
                try:
                    mes_anterior = (self.mes - timezone.timedelta(days=1)).replace(day=1)
                    ultima_del_mes_anterior = Transaccion.objects.filter(mes=mes_anterior).latest('fecha_creacion')
                    saldo_anterior = ultima_del_mes_anterior.saldo_acumulado
                except Transaccion.DoesNotExist:
                    saldo_anterior = 0
                self.saldo_acumulado = saldo_anterior + (self.monto if self.tipo == 'entrada' else -self.monto)
        
        # Guardar la transacción
        super().save(*args, **kwargs)
        
        # Actualizar los saldos de las transacciones posteriores si no estamos en modo actualización masiva
        if not kwargs.get('actualizando_saldos', False):
            self.actualizar_saldos_posteriores()

    class Meta:
        ordering = ['-fecha_creacion']
        get_latest_by = 'fecha_creacion'
