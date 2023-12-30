#encoding:utf-8
from main.models import Genero, Album, Usuario, Puntuacion
from datetime import datetime
import json
import csv
import re 
from main.scraping import store_new_albums
from main.whoosh import store_schema
path = "data"

def populateDB():
    #En esta función almaceno todos los datos, hago scraping y almaceno para whoosh toda la base de datos
    Genero.objects.all().delete()
    Album.objects.all().delete()
    Usuario.objects.all().delete()
    Puntuacion.objects.all().delete()
    (g,a) = populateGenresAndAlbums()
    store_new_albums()
    (u, s) = populateUsersAndScores() 
    store_schema()
    return (g,a,u,s)


def genericPopulate(path, model, fields, separator, dateformat=None):
    model.objects.all().delete()
    
    lista=[]
    fileobj=open(path, "r")
    for line in fileobj.readlines():
        rip = line.strip().split(separator)
        if dateformat != None:
            rip[2] = datetime.strptime(rip[2], dateformat)
        lista.append(model(**dict(zip(fields, rip))))
    fileobj.close()
    model.objects.bulk_create(lista)
    return model.objects.count()    



def populateGenresAndAlbums():
    genres=[]
    fileobj=open(path+"\\amazon_music_metadata.csv", "r")
    reader = csv.reader(fileobj)
    first = next(reader)
    first_string = "".join(first)
    first_split = re.findall(r'"([^"]+)"|([^,]+)', first_string)
    pieces = [x[0] or x[1] for x in first_split]
    n = len(pieces)
    for i in range(2,n):
        name = pieces[i].replace('"','').replace("'",'').replace(';','')
        genres.append(Genero(nombre=name))
    Genero.objects.bulk_create(genres)
    for line in fileobj.readlines():
        line = line.replace(';;;', '')
        if line.strip() != '' and line.strip() != ';;;\n': 
            rip = line.strip().split(',')
            album = Album.objects.create(idAlbum=rip[0], nombre=rip[1])
            generos = []
            for i in range(2,n-1):
                if rip[i] == '1.0':
                    generos.append(genres[i-2])
            album.generos.add(*generos)
    fileobj.close() 
    
    return (Genero.objects.count(), Album.objects.count())

def populateUsersAndScores():

    with open('data/Digital_Music_5.json', 'r') as fileobj:
        for line in fileobj.readlines():
            data = json.loads(line)
            try:
                album = Album.objects.get(idAlbum=data['asin'])
                try:
                    u = Usuario.objects.get(idUsuario=data['reviewerID'])
                    if 'reviewerName' in data and u.nombre == 'Anonymous':
                        u.nombre = data['reviewerName']
                        u.save()
                except Usuario.DoesNotExist:
                    u = Usuario.objects.create(idUsuario=data['reviewerID'], nombre= data['reviewerName'] if 'reviewerName' in data else 'Anonymous')
                Puntuacion.objects.create(idUsuario=Usuario.objects.get(idUsuario = u.idUsuario), 
                                        idAlbum=album, 
                                        puntuacion=float(data['overall']),
                                        opinion=data['reviewText'] if 'reviewText' in data else '')        
            except Album.DoesNotExist:
                pass
    return(Usuario.objects.count(), Puntuacion.objects.count())





    

