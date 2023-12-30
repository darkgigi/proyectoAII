from whoosh import index
from whoosh.fields import Schema, TEXT, NUMERIC, KEYWORD
from main.models import Album, Puntuacion, Usuario
import whoosh.qparser as qparser
from whoosh.index import EmptyIndexError
from whoosh.query import NumericRange
from whoosh.query import And
def store_schema():
    album_schema = Schema(id=TEXT(stored=True), name=TEXT(stored=True), genres=KEYWORD(stored=True))
    review_schema = Schema(idUsuario = TEXT(stored=True), nombreUsuario = TEXT(stored=True), 
                           idAlbum = TEXT(stored=True), nombreAlbum = TEXT(stored=True),
                           score = NUMERIC(stored=True), review = TEXT(stored=True))

    ixAlbum = index.create_in("data/album", album_schema)
    writerAlbum = ixAlbum.writer()
    albums = Album.objects.all()
    for album in albums:
        generos = ", ".join([genero.nombre for genero in album.generos.all()])
        writerAlbum.add_document(id=album.idAlbum, name=album.nombre, genres=generos)
    writerAlbum.commit()

    ixReview = index.create_in("data/review", review_schema)
    writerReview = ixReview.writer()
    reviews = Puntuacion.objects.all()
    for opinion in reviews:
        writerReview.add_document(idUsuario=opinion.idUsuario.idUsuario, nombreUsuario = opinion.idUsuario.nombre,
                                  idAlbum=opinion.idAlbum.idAlbum, nombreAlbum=opinion.idAlbum.nombre,
                                  score=opinion.puntuacion, review=opinion.opinion)
    writerReview.commit()


def search_name(name):
    try:
        ix = index.open_dir("data/album")
        searcher = ix.searcher()
        query = qparser.QueryParser("name", ix.schema).parse(str(name))
        results = searcher.search(query, limit=None)
        return [result for result in results]
    except EmptyIndexError:
        return []

def search_genre(genre):
    try:
        ix = index.open_dir("data/album")
        searcher = ix.searcher()
        query = qparser.QueryParser("genres", ix.schema).parse(str(genre))
        results = searcher.search(query, limit=None)
        return [result for result in results]
    except EmptyIndexError:
        return []
    
def search_review(text, score):
    try:
        ix = index.open_dir("data/review")
        searcher = ix.searcher()
        query1 = qparser.MultifieldParser(["idUsuario", "nombreUsuario"], ix.schema).parse(str(text))
        query2 = NumericRange("score", score, None)
        query = And([query1, query2])
        results = searcher.search(query, limit=None)
        return [result for result in results]
    except EmptyIndexError:
        return []
