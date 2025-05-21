from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Transaccion
from .forms import TransaccionForm
from django.utils import timezone
from calendar import monthrange
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.dateparse import parse_datetime

@login_required
def dashboard(request):
    hoy = timezone.now()
    mes_actual = hoy.replace(day=1)
    primer_dia_mes = mes_actual
    ultimo_dia_mes = mes_actual.replace(day=monthrange(mes_actual.year, mes_actual.month)[1])

    # Obtener transacciones ordenadas por fecha de creación
    transacciones_mes = Transaccion.objects.filter(mes=mes_actual).order_by('fecha_creacion')
    
    # Calcular totales
    entradas = transacciones_mes.filter(tipo='entrada').aggregate(Sum('monto'))['monto__sum'] or 0
    salidas = transacciones_mes.filter(tipo='salida').aggregate(Sum('monto'))['monto__sum'] or 0
    saldo_actual = entradas - salidas

    # Obtener el saldo del mes anterior (si existe)
    mes_anterior = (mes_actual - timezone.timedelta(days=1)).replace(day=1)
    try:
        ultima_transaccion_mes_anterior = Transaccion.objects.filter(mes=mes_anterior).latest('fecha_creacion')
        saldo_anterior = ultima_transaccion_mes_anterior.saldo_acumulado
    except Transaccion.DoesNotExist:
        saldo_anterior = 0

    saldo_total = saldo_anterior + saldo_actual
    
    # Recalcular saldos acumulados para el mes actual
    saldo_acumulado = saldo_anterior
    for transaccion in transacciones_mes:
        if transaccion.tipo == 'entrada':
            saldo_acumulado += transaccion.monto
        else:
            saldo_acumulado -= transaccion.monto
        # Actualizar solo si el saldo ha cambiado
        if transaccion.saldo_acumulado != saldo_acumulado:
            transaccion.saldo_acumulado = saldo_acumulado
            transaccion.save(update_fields=['saldo_acumulado'])
    
    # Reordenar por fecha descendente para la vista
    transacciones_mes = transacciones_mes.order_by('-fecha_creacion')

    context = {
        'transacciones': transacciones_mes,
        'entradas': entradas,
        'salidas': salidas,
        'saldo_actual': saldo_actual,
        'saldo_anterior': saldo_anterior,
        'saldo_total': saldo_total,
        'mes_actual': mes_actual,
    }
    return render(request, 'finanzas/dashboard.html', context)

@login_required
def agregar_transaccion(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            transaccion = form.save(commit=False)
            # Asegurarse de que la fecha tenga la zona horaria correcta
            if not timezone.is_aware(transaccion.fecha):
                transaccion.fecha = timezone.make_aware(transaccion.fecha)
            transaccion.mes = transaccion.fecha.replace(day=1)
            transaccion.save()
            messages.success(request, 'Transacción agregada correctamente.')
            return redirect('finanzas:dashboard')
    else:
        # Establecer la fecha y hora actual como valor por defecto
        initial_data = {'fecha': timezone.localtime().strftime('%Y-%m-%dT%H:%M')}
        form = TransaccionForm(initial=initial_data)
    return render(request, 'finanzas/agregar_transaccion.html', {'form': form})

@login_required
def editar_transaccion(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk)
    if request.method == 'POST':
        form = TransaccionForm(request.POST, instance=transaccion)
        if form.is_valid():
            transaccion = form.save(commit=False)
            # Asegurarse de que la fecha tenga la zona horaria correcta
            if not timezone.is_aware(transaccion.fecha):
                transaccion.fecha = timezone.make_aware(transaccion.fecha)
            transaccion.mes = transaccion.fecha.replace(day=1)
            transaccion.save()
            messages.success(request, 'Transacción actualizada correctamente.')
            return redirect('finanzas:dashboard')
    else:
        form = TransaccionForm(instance=transaccion)
    return render(request, 'finanzas/editar_transaccion.html', {'form': form})

@login_required
def eliminar_transaccion(request, pk):
    try:
        transaccion = Transaccion.objects.get(pk=pk)
    except Transaccion.DoesNotExist:
        messages.error(request, 'La transacción que intentas eliminar no existe.')
        return redirect('finanzas:dashboard')
    
    if request.method == 'POST':
        transaccion.delete()
        messages.success(request, 'La transacción ha sido eliminada exitosamente.')
        return redirect('finanzas:dashboard')
    
    return render(request, 'finanzas/eliminar_transaccion.html', {'transaccion': transaccion})
