from django.shortcuts import render
from main.populateDB import populateDB
from main.scraping import *
from main.whoosh import *
from main.forms import AlbumSearchForm, GenreSearchForm, ReviewSearchForm, UserSearchForm, AlbumIDSearchForm
from main.recommendations import *
import shelve
from django.core.paginator import Paginator

def index(request):
    return render(request, 'index.html')

def populate(request):
    if request.method == 'POST':
        complete = 'complete' in request.POST
        genres,albums,users,scores = populateDB(complete)
        context = {'genres': genres, 'albums':albums, 'users': users, 'scores': scores}
        return render(request, 'populate.html', context)
    else:
        return render(request, 'populate.html')

def search_by_name(request):
    if request.method == 'POST':
        form = AlbumSearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['nombre']
            results = search_name(name)
            list_results = [result for result in results]
            context = {'results': list_results, 'form': form}
            return render(request, 'search_by_name.html', context)
        else:
            return render(request, 'search_by_name.html', {'form': form})
    else:
        return render(request, 'search_by_name.html')
    
def search_by_genre(request):
    context= {'genres': Genero.objects.all().order_by('nombre')}
    if request.method == 'POST':
        form = GenreSearchForm(request.POST)
        if form.is_valid():
            genre = form.cleaned_data['nombre']
            results = search_genre(genre)
            context.update({'results': results, 'form': form})
            return render(request, 'search_by_genre.html', context)
        else:
            context.update({'form': form})
            return render(request, 'search_by_genre.html', context)
    else:
        return render(request, 'search_by_genre.html', context)
    
def search_by_review(request):
    if request.method == 'POST':
        form = ReviewSearchForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['nombre']
            score = 0
            if 'score' in request.POST:
                score = int(form.cleaned_data['score'])
            results = search_review(text, score)
            context = {'results': results, 'form': form}
            return render(request, 'search_by_review.html', context)
        else:
            return render(request, 'search_by_review.html', {'form': form})
    else:
        return render(request, 'search_by_review.html')

def search_all_albums(request):
    albums = Album.objects.all().order_by('nombre')
    paginator = Paginator(albums, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'search_all_albums.html', context)

def store_rs(request):
    Prefs={}   
    shelf = shelve.open("data/RS/dataRS.dat")
    reviews = Puntuacion.objects.all()
    for review in reviews:
        user = review.idUsuario.idUsuario
        itemid = review.idAlbum.idAlbum
        score = review.puntuacion
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = score
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf['SimItems']=calculateSimilarItems(Prefs, n=10)
    shelf.close()

    return render(request, 'index.html')

def fcu(request):
    user = None
    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            idUser = form.cleaned_data['usuario']
            try:
                user = Usuario.objects.get(pk=idUser)
            except:
                return render(request, 'fcu.html', {'badid': True})
            shelf = shelve.open("data/RS/dataRS.dat")
            Prefs = shelf['Prefs']
            shelf.close()
            try:
                rankings = getRecommendations(Prefs, idUser)
            except:
                return render(request, 'fcu.html', {'noresults': True})
            recommendations = rankings[:5]
            albums = []
            scores = []
            for recommendation in recommendations:
                albums.append(Album.objects.get(pk=recommendation[1]))
                scores.append(recommendation[0])
            if len(albums) == 0:
                return render(request, 'fcu.html', {'noresults': True})
            context = {'form': form, 'albums': list(zip(albums, scores))}
            return render(request, 'fcu.html', context)
        else:
            return render(request, 'fcu.html', {'form': form})
    else:
        return render(request, 'fcu.html')

def fci(request):
    user = None
    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            idUser = form.cleaned_data['usuario']
            try:
                user = Usuario.objects.get(pk=idUser)
            except:
                return render(request, 'fci.html', {'badid': True})
            shelf = shelve.open("data/RS/dataRS.dat")
            Prefs = shelf['Prefs']
            SimItems = shelf['SimItems']
            shelf.close()
            try:
                rankings = getRecommendedItems(Prefs,SimItems, idUser)
            except:
                return render(request, 'fci.html', {'noresults': True})
            recommendations = rankings[:5]
            albums = []
            scores = []
            for recommendation in recommendations:
                albums.append(Album.objects.get(pk=recommendation[1]))
                scores.append(recommendation[0])
            if len(albums) == 0:
                return render(request, 'fci.html', {'noresults': True})
            context = {'form': form, 'albums': list(zip(albums, scores))}
            return render(request, 'fci.html', context)
        else:
            return render(request, 'fci.html', {'form': form})
    else:
        return render(request, 'fci.html')

def similar_albums(request):
    if request.method == 'POST':
        form = AlbumIDSearchForm(request.POST)
        if form.is_valid():
            idAlbum = form.cleaned_data['id']
            try:
                album = Album.objects.get(pk=idAlbum)
            except:
                return render(request, 'similar_albums.html', {'badid': True})
            shelf = shelve.open("data/RS/dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            if not idAlbum in ItemsPrefs:
                return render(request, 'similar_albums.html', {'noresults': True})
            try:
                similars = topMatches(ItemsPrefs, idAlbum, n=3)
            except:
                return render(request, 'similar_albums.html', {'noresults': True})
            albums = []
            similarity = []
            for recommendation in similars:
                albums.append(Album.objects.get(pk=recommendation[1]))
                similarity.append(recommendation[0])
            if len(albums) == 0:
                return render(request, 'similar_albums.html', {'noresults': True})
            context = {'form': form, 'albums': list(zip(albums, similarity)), 'album': album}
            return render(request, 'similar_albums.html', context)
        else:
            return render(request, 'similar_albums.html', {'form': form})
    else:
        return render(request, 'similar_albums.html')
