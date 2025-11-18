# app_name/views.py

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,  # Ajout de DetailView pour la redirection de l'Update
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Tache
from .forms import TacheForm


# --- Vues Fonctionnelles (Gardées si nécessaires, mais non CRUD) ---

def home(request):
    """Page d'accueil simple, sans logique CRUD."""
    return render(
        request,
        'taches/home.html', {}
    )


# --- Vues Génériques (CRUD) ---

# 1. Lire (Read - Liste) : Remplace la fonction 'liste_taches'
class TacheListView(ListView):
    """Affiche la liste de toutes les tâches."""
    model = Tache
    template_name = 'taches/tache_list.html'
    context_object_name = 'taches'


# 3. Créer (Create)
class TacheCreateView(CreateView):
    """Gère la création d'une nouvelle tâche."""
    model = Tache
    form_class = TacheForm
    template_name = 'taches/tache_form.html'
    success_url = reverse_lazy('tache_list')


# 4. Mettre à jour (Update)
class TacheUpdateView(UpdateView):
    """Gère la modification d'une tâche existante."""
    model = Tache
    form_class = TacheForm
    template_name = 'taches/tache_form.html'

    def get_success_url(self):
        # Redirige vers la vue de détail après une modification réussie
        return reverse_lazy('tache_detail', kwargs={'pk': self.object.pk})


# 5. Supprimer (Delete)
class TacheDeleteView(DeleteView):
    """Gère la suppression d'une tâche."""
    model = Tache
    template_name = 'taches/tache_confirm_delete.html'
    success_url = reverse_lazy('tache_list')