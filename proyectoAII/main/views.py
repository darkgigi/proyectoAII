from django.shortcuts import render
from main.models import Genero, Album, Usuario, Puntuacion
from main.populateDB import populateDB

def index(request):
    return render(request, 'index.html')

def populate(request):
    genres,albums,users,scores = populateDB()
    context = {'genres': genres, 'albums':albums, 'users': users, 'scores': scores}
    return render(request, 'populate.html', context)