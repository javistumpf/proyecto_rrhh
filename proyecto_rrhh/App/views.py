from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from App.forms import FormCandidato
from App.models import Candidato
from App.forms import FormBusqueda
from App.models import Busqueda
from App.forms import FormPostulacion
from App.models import Postulacion



# Create your views here.

def inicio(request):
    return render(request, "App/inicio.html")

def beneficios(request):
    return render(request, "App/beneficios.html")

def proceso(request):
    return render(request, "App/proceso.html")


# Vistas de formularios


def form_candidato(request):
    if request.method == "POST":
        mi_formulario = FormCandidato(request.POST, request.FILES)  # Asegúrate de incluir request.FILES
        if mi_formulario.is_valid():
            informacion = mi_formulario.cleaned_data
            
            # Crear una instancia del modelo Candidato
            nuevo_candidato = Candidato(
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
            nuevo_candidato.save()  # Guardar el nuevo candidato en la base de datos

            return redirect('App:inicio')
    else:
        mi_formulario = FormCandidato()

    return render(request, "App/form_candidato.html", {"mi_formulario": mi_formulario})


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
            nueva_busqueda.save()  # Guardar la nueva búsqueda en la base de datos

            return redirect('App:inicio')
    else:
        mi_formulario = FormBusqueda()

    return render(request, "App/form_busqueda.html", {"mi_formulario": mi_formulario})


@login_required  # Asegúrate de que el usuario esté autenticado
def form_postulacion(request):
    if request.method == "POST":
        mi_formulario = FormPostulacion(request.POST)
        if mi_formulario.is_valid():
            # Crear una nueva instancia de Postulacion
            nueva_postulacion = Postulacion(
                id_busqueda=mi_formulario.cleaned_data['id_busqueda'],
                id_candidato=request.user.candidato, 
                estado='Pendiente'  # Establecer el estado a "Pendiente"
            )
            nueva_postulacion.save()  # Guardar la nueva postulacion en la base de datos

            return redirect('App:inicio')  # Redirigir a otra página después de guardar
    else:
        mi_formulario = FormPostulacion()

    return render(request, "App/form_postulacion.html", {"mi_formulario": mi_formulario})
    
    # Obtener todas las búsquedas activas
    busquedas = Busqueda.objects.filter(estado='Activa')  # Filtrar por estado "Activa"
    return render(request, "App/form_postulacion.html", {"mi_formulario": mi_formulario, "busquedas": busquedas})