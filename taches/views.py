from django.shortcuts import render
from .models import Tache  # Importez votre modèle


# Assurez-vous d'importer timezone si vous en avez besoin, mais pas ici pour le QuerySet simple

def liste_taches(request):
    # 1. Récupération des données (QuerySet)
    taches = Tache.objects.all().order_by('date_creation')

    # 2. Utilisation de la fonction render
    return render(
        request,
        'taches/liste_taches.html',  {'taches': taches}  # Contexte : les données à envoyer au template
    )

def home(request):

    return render(
        request,
         'taches/home.html',{}
    )