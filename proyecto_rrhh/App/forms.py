from django import forms
from App.models import Busqueda
from App.models import Postulacion
from App.models import Candidato  # Asegúrate de importar el modelo Candidato



## Candidato
class FormCandidato(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = [
            'nombre',
            'apellido',
            'email',
            'telefono',
            'fecha_nacimiento',
            'ciudad',
            'provincia',
            'categoria',
            'seniority',
            'archivo_cv'
        ]

## Búsqueda
class FormBusqueda(forms.Form):
    puesto = forms.CharField(max_length=100, label="Puesto")
    fecha_inicio = forms.DateField(label="Fecha de Inicio")
    fecha_fin = forms.DateField(label="Fecha de Fin")
    categoria = forms.ChoiceField(choices=[
        ('Programación', 'Programación'),
        ('Data', 'Data'),
        ('Redes', 'Redes'),
        ('QA', 'QA'),
        ('UX/UI', 'UX/UI'),
    ], label="Categoría")
    seniority = forms.ChoiceField(choices=[
        ('Junior', 'Junior'),
        ('Semi Senior', 'Semi Senior'),
        ('Senior', 'Senior'),
        ('Manager', 'Manager'),
    ], label="Seniority")
    tareas = forms.CharField(widget=forms.Textarea, label="Tareas")
    requisitos_excluyentes = forms.CharField(widget=forms.Textarea, label="Requisitos Excluyentes")
    requisitos_deseables = forms.CharField(widget=forms.Textarea, label="Requisitos Deseables")
    estado = forms.ChoiceField(choices=[
        ('Activa', 'Activa'),
        ('Finalizada', 'Finalizada')
    ], label="Estado")

## Postulación
class FormPostulacion(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = ['id_busqueda']  # Solo incluimos el campo de búsqueda
        widgets = {
            'id_busqueda': forms.Select(),  # Esto generará un menú desplegable
        }