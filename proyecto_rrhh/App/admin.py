from django.contrib import admin

# Register your models here.

from .models import Candidato, Busqueda, Postulacion

@admin.register(Candidato)
class CandidatoAdmin (admin.ModelAdmin):
    list_display = ["id", "nombre", "apellido", "categoria", "seniority"]
    ordering = ["categoria", "seniority"]
    search_fields = ["nombre", "apellido"]
    list_filter = ["categoria", "seniority"]

@admin.register(Busqueda)
class BusquedaAdmin (admin.ModelAdmin):
    list_display = ["id", "puesto", "categoria", "seniority", "estado"]
    ordering = ["estado","categoria", "seniority"]
    search_fields = ["puesto",]
    list_filter = ["estado", "categoria", "seniority"]

@admin.register(Postulacion)
class PostulacionAdmin (admin.ModelAdmin):
    list_display = ["id", "id_busqueda", "id_candidato", "estado"]
    ordering = ["id_busqueda","estado"]
    search_fields = ["id_busqueda", "id_candidato"]
    list_filter = ["id_busqueda", "id_candidato", "estado"]

