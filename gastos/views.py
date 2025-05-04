from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.defaults import page_not_found, server_error

# Manejo de errores
def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)
