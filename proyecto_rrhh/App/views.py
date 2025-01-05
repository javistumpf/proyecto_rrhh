from django.shortcuts import render

# Create your views here.

def inicio(request):
    return render(request, "App/inicio.html")

def beneficios(request):
    return render(request, "App/beneficios.html")