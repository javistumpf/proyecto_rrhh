from django.urls import path
from users import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', views.login_request, name="Login"),
    path('register/', views.register, name="Register"),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name="Logout"),
    path('editar_usuario/', views.editar_usuario, name='EditarUsuario'),
    path('cambiar_contrasenia', views.CambiarContrasenia.as_view(),name='CambiarContrasenia')
    ]
