from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Genero(models.Model):
    idGenero = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Album(models.Model):
    idAlbum = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=50)
    generos = models.ManyToManyField(Genero)

    def __str__(self):
        return self.nombre + " (" + self.idAlbum + ")"

class Usuario(models.Model):
    idUsuario = models.CharField(primary_key=True, max_length=14)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre + " (" + self.idUsuario + ")"

class Puntuacion(models.Model):
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    idAlbum = models.ForeignKey(Album, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])