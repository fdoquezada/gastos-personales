from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from finanzas.models import Transaccion

class Command(BaseCommand):
    help = 'Actualiza los saldos acumulados de todas las transacciones'

    def handle(self, *args, **options):
        with transaction.atomic():
            try:
                # Obtener todos los meses únicos con transacciones
                meses = Transaccion.objects.dates('mes', 'month', order='ASC')
                
                saldo_anterior = 0
                
                for mes in meses:
                    self.stdout.write(f'Procesando mes: {mes}')
                    # Obtener transacciones del mes ordenadas por fecha de creación
                    transacciones = Transaccion.objects.filter(mes=mes).order_by('fecha_creacion')
                    
                    saldo_mes = saldo_anterior
                    
                    for transaccion in transacciones:
                        # Calcular el saldo acumulado
                        if transaccion.tipo == 'entrada':
                            saldo_mes += transaccion.monto
                        else:
                            saldo_mes -= transaccion.monto
                        
                        # Actualizar solo si el saldo ha cambiado
                        if transaccion.saldo_acumulado != saldo_mes:
                            # Actualizar directamente en la base de datos para evitar bucles
                            Transaccion.objects.filter(pk=transaccion.pk).update(
                                saldo_acumulado=saldo_mes
                            )
                    
                    saldo_anterior = saldo_mes
                
                self.stdout.write(self.style.SUCCESS('Saldos actualizados correctamente'))
                
                # Actualizar los saldos de las transacciones posteriores para la última transacción
                if transacciones.exists():
                    ultima_transaccion = transacciones.last()
                    ultima_transaccion.actualizar_saldos_posteriores()
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error al actualizar saldos: {str(e)}'))
                raise
