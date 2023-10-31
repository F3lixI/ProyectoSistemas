from django import forms
from .models import Comentario, Pelicula

class ComentarioForm(forms.ModelForm):
    """Fromulario para la creacion de comentarios"""
    class Meta:
        model = Comentario
        fields = ['texto']

class PeliculaForm(forms.ModelForm):
    """Formulario para la creacion de peliculas"""
    class Meta:
        model = Pelicula
        fields = ['titulo', 'director']
        
    def clean_titulo(self):
        """Limpia los datos para evitar ejecucion remota, y verifica si la pelicula existe"""
        titulo = self.cleaned_data.get('titulo')
        if Pelicula.objects.filter(titulo__iexact=titulo).exists():
            raise forms.ValidationError("Una película con este título ya existe.")
        return titulo
    