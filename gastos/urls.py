"""
URL configuration for gastos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404, handler500

# Funciones para manejo de errores
handler404 = 'home.views.error_404'
handler500 = 'home.views.error_500'

from errors.views import handler404 as custom_handler404
from errors.views import handler500 as custom_handler500
from errors.views import logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('finanzas/', include('finanzas.urls')),
    path('auth/', include('atentication.urls')),
    path('logout/', logout_view, name='logout'),
]

# Manejo de errores
handler404 = custom_handler404
handler500 = custom_handler500
