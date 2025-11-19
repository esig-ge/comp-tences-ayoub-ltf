from django import forms
from django.forms import ModelForm

from .models import Tache

class TacheForm(ModelForm):
    class Meta:
        model = Tache
        fields = ('titre', 'description', 'date_due', 'completee','statut_en_cours')

