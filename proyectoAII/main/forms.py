from django import forms


class AlbumSearchForm(forms.Form):
    nombre = forms.CharField(max_length=200, required=True, label='Buscar por nombre')
