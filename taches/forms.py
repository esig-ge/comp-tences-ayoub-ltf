from django import forms
from .models import Tache

class TacheForm(forms.Form):
    model = Tache
    fields = ['titre', 'description', 'date_due', 'completee']