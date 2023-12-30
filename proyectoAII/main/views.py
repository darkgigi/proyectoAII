from django.shortcuts import render
from main.populateDB import populateDB
from main.scraping import *
from main.whoosh import *
from main.forms import AlbumSearchForm, GenreSearchForm, ReviewSearchForm

def index(request):
    return render(request, 'index.html')

def populate(request):
    if request.method == 'POST':
        genres,albums,users,scores = populateDB()
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