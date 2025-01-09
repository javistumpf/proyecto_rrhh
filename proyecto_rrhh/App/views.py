from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from App.forms import FormCandidato
from App.models import Candidato
from App.forms import FormBusqueda
from App.models import Busqueda
from App.forms import FormPostulacion
from App.models import Postulacion
from django.http import HttpResponseNotFound
from django.contrib import messages  # Importar el sistema de mensajes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView


# Create your views here.

## Inicio
def inicio(request):
    return render(request, "App/inicio.html")

## Beneficios

def beneficios(request):
    return render(request, "App/beneficios.html")

## Proceso

def proceso(request):
    return render(request, "App/proceso.html")

## About

def about(request):
    return render(request, "App/about.html")


# Vistas de formularios

## Form candidato

@login_required  
def form_candidato(request):
    if request.method == "POST":
        mi_formulario = FormCandidato(request.POST, request.FILES) 
        if mi_formulario.is_valid():
            informacion = mi_formulario.cleaned_data
            
            # Crear una instancia del modelo Candidato y asociar el usuario logueado
            nuevo_candidato = Candidato(
                user=request.user,  
                nombre=informacion["nombre"],
                apellido=informacion["apellido"],
                email=informacion["email"],
                telefono=informacion["telefono"],
                fecha_nacimiento=informacion["fecha_nacimiento"],
                ciudad=informacion["ciudad"],
                provincia=informacion["provincia"],
                categoria=informacion["categoria"],
                seniority=informacion["seniority"],
                archivo_cv=informacion["archivo_cv"]
            )
            nuevo_candidato.save()  
            
            
            messages.success(request, 'Candidato creado exitosamente.')

            return render(request, "App/form_candidato.html", {"mi_formulario": mi_formulario}) 
    else:
        mi_formulario = FormCandidato()

    return render(request, "App/form_candidato.html", {"mi_formulario": mi_formulario})


## Búsqueda

def form_busqueda(request):
    if request.method == "POST":
        mi_formulario = FormBusqueda(request.POST)
        if mi_formulario.is_valid():
            informacion = mi_formulario.cleaned_data
            
            # Crear una instancia del modelo Busqueda
            nueva_busqueda = Busqueda(
                puesto=informacion["puesto"],
                fecha_inicio=informacion["fecha_inicio"],
                fecha_fin=informacion["fecha_fin"],
                categoria=informacion["categoria"],
                seniority=informacion["seniority"],
                tareas=informacion["tareas"],
                requisitos_excluyentes=informacion["requisitos_excluyentes"],
                requisitos_deseables=informacion["requisitos_deseables"],
                estado=informacion["estado"]
            )
            nueva_busqueda.save()  

            return redirect('App:inicio')
    else:
        mi_formulario = FormBusqueda()

    return render(request, "App/form_busqueda.html", {"mi_formulario": mi_formulario})

## Postulación

@login_required  
def form_postulacion(request):
    try:
        candidato = request.user.candidato  
    except Candidato.DoesNotExist:
        messages.warning(request, 'Debes crear un perfil de candidato antes de postularte.')  
        return redirect('FormCandidato')  

    if request.method == "POST":
        mi_formulario = FormPostulacion(request.POST)
        if mi_formulario.is_valid():
            nueva_postulacion = Postulacion(
                id_busqueda=mi_formulario.cleaned_data['id_busqueda'],
                id_candidato=candidato,  
                estado='Pendiente'
            )
            nueva_postulacion.save()  
            
            messages.success(request, 'Postulación realizada exitosamente.')

            return redirect('mis_postulaciones') 

    else:
        id_busqueda = request.GET.get('id_busqueda')
        puesto = request.GET.get('puesto')
        if id_busqueda:
            mi_formulario = FormPostulacion(initial={'id_busqueda': id_busqueda})  
        else:
            mi_formulario = FormPostulacion()

    return render(request, "App/form_postulacion.html", {
        "mi_formulario": mi_formulario,
        "puesto": puesto
    })

    ## Obtener todas las búsquedas activas
    busquedas = Busqueda.objects.filter(estado='Activa')  # Filtrar por estado "Activa"
    return render(request, "App/form_postulacion.html", {"mi_formulario": mi_formulario, "busquedas": busquedas})

# Vistas basadas en clases

## Búsqueda
class BusquedaListView(ListView):
    model = Busqueda
    template_name = 'App/lista_busquedas.html'  
    context_object_name = 'busquedas' 
    def get_queryset(self):
        queryset = Busqueda.objects.filter(estado='Activa')

        categoria = self.request.GET.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria=categoria)

        seniority = self.request.GET.get('seniority')
        if seniority:
            queryset = queryset.filter(seniority=seniority)

        return queryset
    

## Detalle de búsqueda 

def detalle_busqueda(request, id):
    try:
        busqueda = Busqueda.objects.get(id=id)  
    except Busqueda.DoesNotExist:
        return HttpResponseNotFound("La búsqueda no existe.")  

    return render(request, 'App/detalle_busqueda.html', {'busqueda': busqueda})

# Vistas login required

## Mis postulaciones

@login_required
def mis_postulaciones(request):
    try:
        candidato = request.user.candidato  
    except Candidato.DoesNotExist:
        messages.warning(request, 'Debes crear un perfil de candidato antes de ver tus postulaciones.')  
        return redirect('FormCandidato')  

    postulaciones = Postulacion.objects.filter(id_candidato=candidato) 

    return render(request, "App/mis_postulaciones.html", {"postulaciones": postulaciones})

    
## Ver perfil

@login_required
def ver_perfil(request):
    try:
        candidato = request.user.candidato 
    except Candidato.DoesNotExist:
        messages.warning(request, 'Debes crear un perfil de candidato antes de ver tu perfil.')  
        return redirect('FormCandidato')  

    return render(request, "App/ver_perfil.html", {"candidato": candidato})

## Editar perfil

@login_required
def editar_perfil(request):
    candidato = request.user.candidato 

    if request.method == "POST":
        form = FormCandidato(request.POST, request.FILES, instance=candidato) 
        if form.is_valid():
            form.save()  
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('ver_perfil') 
    else:
        form = FormCandidato(instance=candidato) 

    return render(request, "App/candidato_form.html", {"form": form})