from django.shortcuts import render, redirect,get_object_or_404
from .models import Tache, Commentaire
from .forms import TacheForm
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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


def tache_detail(request, pk):
    """
    1. Récupère la tâche demandée grâce à l'ID (pk) dans l'URL.
    2. Renvoie le fichier HTML 'detail_tache.html'.
    """
    tache = get_object_or_404(Tache, pk=pk)

    # On passe la variable 'tache' au template pour l'afficher
    return render(request, 'taches/detail_tache.html', {'tache': tache})



def ajouter_commentaire_ajax(request):
    """
    Cette vue reçoit une requête AJAX (POST), crée un commentaire en BDD
    et renvoie les données du nouveau commentaire en JSON.
    """
    if request.method == 'POST':
        # 1. On décode les données JSON envoyées par le JS
        data = json.loads(request.body)
        contenu = data.get('contenu')
        tache_id = data.get('tache_id')

        # 2. On sauvegarde en BDD (Dialogue BDD)
        tache = Tache.objects.get(id=tache_id)
        nouveau_com = Commentaire.objects.create(tache=tache, contenu=contenu)

        # 3. On renvoie une réponse JSON (Client <-> Serveur)
        return JsonResponse({
            'status': 'success',
            'contenu': nouveau_com.contenu,
            'date': nouveau_com.date_creation.strftime("%d/%m/%Y")
        })

    return JsonResponse({'status': 'error'}, status=400)
