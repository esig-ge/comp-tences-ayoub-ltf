from django.contrib import admin
from .models import Tache # Importation du modèle Tache

# Enregistrement de mon modèle ici
admin.site.register(Tache)
