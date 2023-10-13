from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.username
    
from django.db import models

class Pelicula(models.Model):
    titulo = models.CharField(max_length=200)
    año_lanzamiento = models.PositiveIntegerField()
    genero = models.CharField(max_length=100)
    director = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo
    
class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario.usuario.username} en {self.pelicula.titulo}"

