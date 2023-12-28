from django.contrib import admin

# Register your models here.

from main.models import Genero, Album, Usuario, Puntuacion

admin.site.register(Genero)
admin.site.register(Album)
admin.site.register(Usuario)
admin.site.register(Puntuacion)