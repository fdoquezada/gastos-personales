from django.urls import path
from . import views

app_name = 'finanzas'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('agregar_transaccion/', views.agregar_transaccion, name='agregar_transaccion'),
    path('editar_transaccion/<int:pk>/', views.editar_transaccion, name='editar_transaccion'),
    path('eliminar_transaccion/<int:pk>/', views.eliminar_transaccion, name='eliminar_transaccion'),
]