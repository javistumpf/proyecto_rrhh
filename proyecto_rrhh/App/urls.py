from django.urls import path
from App import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name="Inicio"),
    path('App/beneficios', views.beneficios, name="Beneficios"),
    path('App/proceso', views.proceso, name="Proceso"),

]

forms_api = [
        path('form_candidato/', views.form_candidato, name="FormCandidato"),
        path('form_busqueda/', views.form_busqueda, name="FormBusqueda"),
        path('form_postulacion/', views.form_postulacion, name="FormPostulacion"),
]

urlpatterns += forms_api

# Solo en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

