from django import forms
from django.forms import ModelForm

from .models import Tache

class TacheForm(ModelForm):
    class Meta:
        model = Tache
        fields = ('titre', 'description', 'date_due')
        labels = {'titre' : 'Titre','description':'Description','date_due': 'Date', }

        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date_due': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }