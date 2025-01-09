from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from users.forms import UserRegisterForm
from users.forms import UserEditForm
from .models import Avatar
from .forms import UserEditForm

# Create your views here.

## Login

def login_request(request):

    msg_login = ""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            usuario = form.cleaned_data.get('username')
            contrasenia = form.cleaned_data.get('password')

            user = authenticate(username=usuario, password=contrasenia)

            if user is not None:
                login(request, user)
                return render(request, "App/inicio.html")

        msg_login = "Usuario o contraseña incorrectos"

    form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form, "msg_login": msg_login})

## Registro

def register(request):

    msg_register = ""
    if request.method == 'POST':

        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Login') 
        
        msg_register = "Error en los datos ingresados"

    form = UserRegisterForm()     
    return render(request,"users/registro.html" ,  {"form":form, "msg_register": msg_register})


## Editar usuario

@login_required
def editar_usuario(request):
    usuario = request.user

    try:
        avatar = usuario.avatar 
    except Avatar.DoesNotExist:
        avatar = None  

    if request.method == 'POST':
        miFormulario = UserEditForm(request.POST, request.FILES, instance=usuario)

        if miFormulario.is_valid():
            
            miFormulario.save()

            if miFormulario.cleaned_data.get("imagen"):
                if avatar is None:
                    
                    avatar = Avatar(user=usuario)
                avatar.imagen = miFormulario.cleaned_data.get("imagen")
                avatar.save()  

            
            return render(request, "App/inicio.html")

    else:
        miFormulario = UserEditForm(instance=usuario)

    return render(
        request,
        "users/editar_usuario.html",
        {
            "mi_form": miFormulario,
            "usuario": usuario,
            "avatar": avatar  
        }
    )

## Cambiar contraseña
class CambiarContrasenia(LoginRequiredMixin, PasswordChangeView):

    template_name = "users/cambiar_contrasenia.html"
    success_url = reverse_lazy('EditarUsuario')