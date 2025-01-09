from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from App import views
from .views import BusquedaListView
from .views import detalle_busqueda
from .views import mis_postulaciones
from .views import ver_perfil, editar_perfil



urlpatterns = [
    path('', views.inicio, name="Inicio"),
    path('App/beneficios', views.beneficios, name="Beneficios"),
    path('App/proceso', views.proceso, name="Proceso"),
    path('App/about', views.about, name="About"),
    path('App/lista_busquedas', BusquedaListView.as_view(), name='lista_busquedas'),
    path('App/detalle_busqueda/<int:id>/', detalle_busqueda, name='detalle_busqueda'),
    path('App/mis_postulaciones/', mis_postulaciones, name='mis_postulaciones'),
    path('App/perfil/', ver_perfil, name='ver_perfil'),
    path('App/editar_perfil/', editar_perfil, name='editar_perfil'),
]

forms_api = [
        path('form_candidato/', views.form_candidato, name="FormCandidato"),
        path('form_busqueda/', views.form_busqueda, name="FormBusqueda"),
        path('form_postulacion/', views.form_postulacion, name="FormPostulacion"),
]

urlpatterns += forms_api

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

