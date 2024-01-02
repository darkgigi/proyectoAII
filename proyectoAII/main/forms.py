from django import forms
from .models import Genero

class AlbumSearchForm(forms.Form):
    nombre = forms.CharField(max_length=200, required=True, label='Buscar por nombre')

class GenreSearchForm(forms.Form):
    nombre = forms.ModelChoiceField(queryset=Genero.objects.all(), empty_label="Seleccione un género")

class ReviewSearchForm(forms.Form):
    nombre = forms.CharField(max_length=200, required=True, label='Buscar por nombre')
    score = forms.IntegerField(required=False, label='Buscar por score')

class UserSearchForm(forms.Form):
    usuario = forms.CharField(max_length=200, required=True, label='Buscar por nombre')

class AlbumIDSearchForm(forms.Form):
    id = forms.CharField(max_length=10, required=True, label='Buscar por ID')