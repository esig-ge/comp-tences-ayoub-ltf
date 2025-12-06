from django.shortcuts import render, redirect,get_object_or_404
from .models import Tache, Commentaire
from .forms import TacheForm
import json
from django.http import JsonResponse

def home(request):
    return render(
        request,
        'taches/home.html', {}
    )

def liste_view(request):
    taches_existantes= Tache.objects.all().order_by('date_creation')
    contexte = {'taches':taches_existantes}
    return render(
        request,
        'taches/tache.html',
        contexte)


def tache_create(request):
    """PRG (Post/Redirect/Get) pour éviter la double soumission."""

    form = TacheForm(request.POST or None)

    if form.is_valid():
        form.save() # Sauvegarde la nouvelle tâche dans la base de données
        return redirect('tache')

    return render(
        request,
        'taches/tache_creation.html', # Le template qui affiche le formulaire
        {'form': form}
    )



def tache_update(request, pk):
    """ on récupère la tâche par son identifiant """
    tache = get_object_or_404(Tache, pk=pk)
    form = TacheForm(request.POST or None, instance=tache)
    if form.is_valid():
        form.save()
        return redirect('tache')
    #rendre le même template de formulaire pré-rempli
    return render(
        request,
        'taches/tache_creation.html', {'form': form,'tache': tache}
    )

def tache_delete(request, pk):
    tache = get_object_or_404(Tache, pk=pk)
    if request.method == 'POST':
        tache.delete()
        return redirect('tache')
    return render(
        request,
        'taches/confirmer_suppression.html',{'tache':tache}
    )

def tache_statut(request, pk):
    tache = get_object_or_404(Tache, pk=pk)
    tache.statut_en_cours= not tache.statut_en_cours
    tache.save()
    return redirect('tache')


def api_create_tache(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        titre_recu = data.get('titre')

        if titre_recu:
            tache = Tache.objects.create(titre = titre_recu)

        return JsonResponse({
           'status' : 'ok' ,'id' : tache.id , 'titre' : tache.titre
        })



