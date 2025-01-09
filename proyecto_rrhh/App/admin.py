from django.contrib import admin
from .models import Candidato, Busqueda, Postulacion

# Register your models here.

# Candidato
@admin.register(Candidato)
class CandidatoAdmin (admin.ModelAdmin):
    list_display = ["id", "nombre", "apellido", "categoria", "seniority"]
    ordering = ["categoria", "seniority"]
    search_fields = ["nombre", "apellido"]
    list_filter = ["categoria", "seniority"]

# Búsqueda
@admin.register(Busqueda)
class BusquedaAdmin (admin.ModelAdmin):
    list_display = ["id", "puesto", "categoria", "seniority",  "fecha_fin","estado",]
    list_editable = ["estado"]  # Hacer el campo 'estado' editable directamente

    ordering = ["estado","categoria", "seniority"]
    search_fields = ["puesto",]
    list_filter = ["estado", "categoria", "seniority"]

# Postulación
@admin.register(Postulacion)
class PostulacionAdmin(admin.ModelAdmin):
    list_display = ["id", "get_busqueda", "get_candidato_nombre", "fecha_postulacion", "estado"]
    list_editable = ["estado"]
    ordering = ["id_busqueda", "estado"]
    search_fields = ["id_busqueda__puesto", "id_candidato__nombre", "id_candidato__apellido"]
    list_filter = ["id_busqueda", "id_candidato", "estado"]

    def get_busqueda(self, obj):
        return obj.id_busqueda.puesto  

    def get_candidato_nombre(self, obj):
        return f"{obj.id_candidato.nombre} {obj.id_candidato.apellido}" 

    get_busqueda.short_description = 'Búsqueda'
    get_candidato_nombre.short_description = 'Candidato'
