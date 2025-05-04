from django import forms
from .models import Transaccion

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['fecha', 'descripcion', 'tipo', 'monto']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }