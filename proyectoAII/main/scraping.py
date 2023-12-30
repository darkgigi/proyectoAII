from bs4 import BeautifulSoup
import os, ssl
from urllib import request
import random, string
from main.models import Genero, Album


if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

def store_new_albums():

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
        

def gen_random_id():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(9))