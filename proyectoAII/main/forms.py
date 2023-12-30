from django import forms
from .models import Genero

class AlbumSearchForm(forms.Form):
    nombre = forms.CharField(max_length=200, required=True, label='Buscar por nombre')

class GenreSearchForm(forms.Form):
    nombre = forms.ModelChoiceField(queryset=Genero.objects.all(), empty_label="Seleccione un género")