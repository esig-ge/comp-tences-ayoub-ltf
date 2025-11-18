from django.shortcuts import render, redirect  # Import de 'redirect' pour le PRG
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Tache
from .forms import TacheForm


def home(request):
    return render(
        request,
        'taches/home.html', {}
    )

def liste_taches(request):
    taches_existantes= Tache.objects.all().order_by('date_creation')
    contexte = {'taches':taches_existantes}
    return render(
        request,
        'taches/tache.html',
        contexte)


def tacheCreate(request):
    """PRG (Post/Redirect/Get) pour éviter la double soumission."""

    form = TacheForm(request.POST or None)

    if form.is_valid():
        form.save() # Sauvegrde la nouvelle tâche dans la base de données
        return redirect('tache_list') 

    return render(
        request,
        'taches/tache_creation.html', # Le template qui affiche le formulaire
        {'form': form}
    )


# ----------------------------------------------------
# VUES BASÉES SUR DES CLASSES (CBVs) - Pour référence future
# ----------------------------------------------------

# 1. Lire (Read - Liste)
class TacheListView(ListView):
    """Affiche la liste de toutes les tâches."""
    model = Tache
    template_name = 'taches/tache_list.html'
    context_object_name = 'taches'


# 2. Créer (Create)
class TacheCreateView(CreateView):
    """Gère la création d'une nouvelle tâche."""
    model = Tache
    form_class = TacheForm
    template_name = 'taches/tache_creation.html' # Utilise le même template
    success_url = reverse_lazy('tache_list')


# 3. Mettre à jour (Update)
class TacheUpdateView(UpdateView):
    """Gère la modification d'une tâche existante."""
    model = Tache
    form_class = TacheForm
    template_name = 'taches/tache_creation.html'

    def get_success_url(self):
        # Redirige vers la liste après une modification réussie
        return reverse_lazy('tache_list')


# 4. Supprimer (Delete)
class TacheDeleteView(DeleteView):
    """Gère la suppression d'une tâche."""
    model = Tache
    template_name = 'taches/tache_confirm_delete.html'
    success_url = reverse_lazy('tache_list')