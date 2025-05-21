from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def error_404(request, exception):
    return render(request, '404.html', status=404)

def error_500(request):
    return render(request, '500.html', status=500)
