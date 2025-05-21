from django import forms
from .models import Transaccion
from django.utils import timezone

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['fecha', 'descripcion', 'tipo', 'monto']
        widgets = {
            'fecha': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'step': '1'  # Permite segundos
                },
                format='%Y-%m-%dT%H:%M'  # Formato compatible con datetime-local
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si es una instancia existente, formatear la fecha para el input
        if self.instance and self.instance.pk:
            self.initial['fecha'] = self.instance.fecha.strftime('%Y-%m-%dT%H:%M')