from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Candidato(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Permitir nulos temporalmente
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField()
    ciudad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=[
        ('Programación', 'Programación'),
        ('Data', 'Data'),
        ('Redes', 'Redes'),
        ('QA', 'QA'),
        ('UX/UI', 'UX/UI'),
        ])
    seniority= models.CharField(max_length=50, choices=[
        ('Junior', 'Junior'),
        ('Semi Senior', 'Semi Senior'),
        ('Senior', 'Senior'),
        ('Manager', 'Manager'),
        ])
    archivo_cv = models.FileField(upload_to='cvs/')

class Busqueda(models.Model):
    puesto = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    categoria = models.CharField(max_length=50, choices=[
        ('Programación', 'Programación'),
        ('Data', 'Data'),
        ('Redes', 'Redes'),
        ('QA', 'QA'),
        ('UX/UI', 'UX/UI'),
        ])
    seniority= models.CharField(max_length=50, choices=[
        ('Junior', 'Junior'),
        ('Semi Senior', 'Semi Senior'),
        ('Senior', 'Senior'),
        ('Manager', 'Manager'),
        ])
    tareas= models.TextField()
    requisitos_excluyentes = models.TextField()
    requisitos_deseables = models.TextField()
    estado = models.CharField(max_length=50, choices=[
        ('Activa', 'Activa'),
        ('Finalizada', 'Finalizada')
        ])

class Postulacion(models.Model):
    id_busqueda = models.ForeignKey(Busqueda, on_delete=models.CASCADE, related_name="postulaciones")
    id_candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, related_name="postulaciones")
    fecha_postulacion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=[
        ('Pendiente', 'Pendiente'),
        ('Prueba técnica', 'Prueba técnica'),
        ('Entrevistas', 'Entrevistas'),
        ('Preocupacional', 'Preocupacional'),
        ('Contratado', 'Contratado'),
        ('Rechazado', 'Rechazado')
        ])
