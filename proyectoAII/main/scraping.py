from bs4 import BeautifulSoup
import os, ssl
from urllib import request
import random, string
from main.models import Genero, Album, Usuario, Puntuacion


if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

def store_new_albums_and_reviews():

    url = "https://www.albumoftheyear.org/releases/this-week/"

    headers = {'User-Agent': 'Mozilla/5.0'}
    req = request.Request(url, headers=headers)
    response = request.urlopen(req)
    soup = BeautifulSoup(response, 'html.parser')
    albums = soup.find_all('div', class_='albumBlock five small')

    for album in albums:
        idAlbum = gen_random_id()
        enlace = album.find('a').get('href')
        name = album.find('div', class_='albumTitle').getText()
        try:
            Album.objects.get(nombre=name)
        except:
            pass
        headers = {'User-Agent': 'Mozilla/5.0'}
        req2 = request.Request("https://www.albumoftheyear.org"+ enlace, headers=headers)
        response2 = request.urlopen(req2)
        soup2 = BeautifulSoup(response2, 'html.parser')
        genres = soup2.find_all('meta', attrs= {'itemprop': "genre"})
        genres_text = [genre.get('content') for genre in genres if genre.get('content')]
        objects = []
        for genre in genres_text:
            object,_ = Genero.objects.get_or_create(nombre=genre)
            objects.append(object)
        album = Album.objects.create(idAlbum=idAlbum, nombre=name)
        album.generos.set(objects)
        album.save()
        reqreviews = request.Request("https://www.albumoftheyear.org"+ enlace.replace('.php','/user-reviews'), headers=headers)
        responsereviews = request.urlopen(reqreviews)
        soup3 = BeautifulSoup(responsereviews, 'html.parser')
        reviews = soup3.find_all('div', class_='albumReviewRow')
        
        for review in reviews:
            if review.find('div', class_='ratingBlock') == None: continue
            rate = review.find('div', class_='ratingBlock').find('span', {'itemprop':'ratingValue'}).getText()
            if rate == 'NR': continue
            score = float(rate)
            username = review.find('div',class_="userReviewName").find('span').getText()
            normalized_score = normalize_score(score)
            text_elements = review.find('div', class_='albumReviewText').find_all('p')
            text = ' '.join(p.getText() for p in text_elements)
            try:
                user = Usuario.objects.get(nombre=username)
            except Usuario.DoesNotExist:
                user = Usuario.objects.create(idUsuario=gen_random_id(user=True), nombre=username)
            Puntuacion.objects.create(idUsuario=user, idAlbum = album, puntuacion=normalized_score, opinion=text)
        

def gen_random_id(user=False):
    #Función reutilizable para generar ids aleatorios de longitud 9 o 13 dependiendo de si es para un usuario o para un album nuevo
    n = 13 if user else 9
    id= ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))
    exists = Album.objects.filter(idAlbum=id).exists() if not user else Usuario.objects.filter(idUsuario=id).exists()
    while exists:
        id= ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))
        exists = Album.objects.filter(idAlbum=id).exists() if not user else Usuario.objects.filter(idUsuario=id).exists()
    return id

def normalize_score(score):
    return score / 20 