from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.template import loader
from django.http import HttpResponse
from django.views.defaults import page_not_found, server_error

# Create your views here.

# Manejo de errores
def handler404(request, exception=None):
    template = loader.get_template('errors/404.html')
    return HttpResponse(template.render({}, request), status=404)

def handler500(request):
    template = loader.get_template('errors/500.html')
    return HttpResponse(template.render({}, request), status=500)

# Vista para logout
def logout_view(request):
    auth_logout(request)
    return redirect('home')
