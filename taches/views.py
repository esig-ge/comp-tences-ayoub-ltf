from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.template.defaultfilters import date as django_date_filter
import json

from .forms import TacheForm
from .models import Tache


# --- VUES GÉNÉRALES ---

def home(request):
    return render(request, 'taches/home.html', {})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tache')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# --- VUES DE GESTION DES TÂCHES ---

@login_required
def liste_view(request):
    taches_existantes = Tache.objects.filter(user=request.user).order_by('date_creation')
    return render(request, 'taches/tache.html', {'taches': taches_existantes})


@login_required
def tache_create(request):
    form = TacheForm(request.POST or None)

    if form.is_valid():
        tache = form.save(commit=False)
        tache.user = request.user

        tache.save()
        return redirect('tache')

    return render(request, 'taches/tache_creation.html', {'form': form})


@login_required
def tache_update(request, pk):

    tache = get_object_or_404(Tache, pk=pk)

    form = TacheForm(request.POST or None, instance=tache)
    if form.is_valid():
        form.save()
        return redirect('tache')

    return render(request, 'taches/tache_creation.html', {'form': form, 'tache': tache})


@login_required
def tache_statut(request, pk):
    tache = get_object_or_404(Tache, pk=pk)
    tache.statut_en_cours = not tache.statut_en_cours
    tache.save()
    return redirect('tache')


# --- VUE VULNÉRABLE  ---

@login_required

def tache_delete(request, pk):
    tache = get_object_or_404(Tache, pk=pk)
    if request.method == 'POST':
        tache.delete()

    return redirect('tache')


# --- API ---

def api_create_tache(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            titre_recu = data.get('titre')
            desc_recue = data.get('description')
            date_due_recue = data.get('date_due')

            if titre_recu:
                tache = Tache.objects.create(
                    titre=titre_recu,
                    description=desc_recue or '',
                    date_due=date_due_recue or None,
                    statut_en_cours=True
                    # Note : L'API crée des tâches sans utilisateur ici (user=None)
                )
                tache.refresh_from_db()

                if tache.date_due:
                    date_formatee = str(django_date_filter(tache.date_due, "j F Y H:i"))
                else:
                    date_formatee = None

                return JsonResponse({
                    'status': 'ok',
                    'id': tache.id,
                    'titre': tache.titre,
                    'description': tache.description,
                    'date_due': date_formatee,
                })

            return JsonResponse({'status': 'erreur: champs manquants'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'erreur: JSON invalide'}, status=400)

    return JsonResponse({'status': 'erreur: méthode non autorisée'}, status=405)