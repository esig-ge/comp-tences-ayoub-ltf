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

from django.conf import settings
from google import genai
from google.genai import types


@login_required
def chat_with_coach(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST requis'}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get('message')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Format JSON invalide'}, status=400)

    # --- 1. DÉFINITION DES OUTILS ---
    def get_current_tasks() -> str:
        """Récupère la liste des tâches de l'utilisateur."""
        taches = Tache.objects.filter(user=request.user, statut_en_cours=True)
        if not taches:
            return "L'utilisateur n'a aucune tâche en cours."
        return "\n".join([f"ID: {t.id} - {t.titre}" for t in taches])

    def add_task(titre: str) -> str:
        """Ajoute une nouvelle tâche."""
        Tache.objects.create(titre=titre, statut_en_cours=True, user=request.user)
        return f"Action réussie : La tâche '{titre}' a été ajoutée."

    def complete_task(task_id: int) -> str:
        """Marque une tâche comme terminée via son ID."""
        try:
            tache = Tache.objects.get(id=task_id, user=request.user)
            tache.statut_en_cours = False
            tache.save()
            return f"Action réussie : La tâche {task_id} est terminée."
        except Tache.DoesNotExist:
            return f"Erreur : Tâche {task_id} introuvable."

    def delete_task(task_id: int) -> str:
        """Supprime définitivement une tâche de la base de données via son ID."""
        try:
            tache = Tache.objects.get(id=task_id, user=request.user)
            titre = tache.titre
            tache.delete()
            return f"Action réussie : La tâche '{titre}' (ID: {task_id}) a été supprimée."
        except Tache.DoesNotExist:
            return f"Erreur : Impossible de trouver la tâche {task_id} pour la supprimer."

    # --- 2. CONFIGURATION GEMINI ---
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    system_instruction = """
    Tu es 'ProCoach', un assistant expert en productivité. 
    Tu dois aider l'utilisateur à gérer ses tâches.
    Si l'utilisateur te demande d'ajouter ou terminer une tâche, utilise tes outils.
    Réponds toujours de manière concise et motivante.
    """

    # CONFIGURATION CRUCIALE : Exécution automatique
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=[get_current_tasks, add_task, complete_task, delete_task],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False),
        temperature=0.7,
    )

    # --- 3. GÉNÉRATION DE LA RÉPONSE ---
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash', # Version à jour
            contents=user_message,
            config=config
        )

        # Le texte final après que l'IA a potentiellement utilisé un outil
        return JsonResponse({'status': 'ok', 'reply': response.text})

    except Exception as e:
        print(f"Erreur Gemini: {str(e)}") # Pour voir l'erreur dans ton terminal
        return JsonResponse({'error': str(e)}, status=500)



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
    # CORRECTION : On vérifie que la tâche appartient bien au "request.user"
    tache = get_object_or_404(Tache, pk=pk, user=request.user)

    form = TacheForm(request.POST or None, instance=tache)
    if form.is_valid():
        form.save()
        return redirect('tache')

    return render(request, 'taches/tache_creation.html', {'form': form, 'tache': tache})


@login_required
def tache_statut(request, pk):
    # CORRECTION : On sécurise ici aussi
    tache = get_object_or_404(Tache, pk=pk, user=request.user)
    tache.statut_en_cours = not tache.statut_en_cours
    tache.save()
    return redirect('tache')


@login_required
def tache_delete(request, pk):
    # CORRECTION : On sécurise contre les suppressions fantômes d'autres utilisateurs
    tache = get_object_or_404(Tache, pk=pk, user=request.user)
    if request.method == 'POST':
        tache.delete()

    return redirect('tache')


# --- API ---

@login_required # CORRECTION : L'API ne doit pas être accessible aux visiteurs anonymes
def api_create_tache(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            titre_recu = data.get('titre')
            desc_recue = data.get('description')
            date_due_recue = data.get('date_due')

            if titre_recu:
                # CORRECTION : L'utilisateur connecté est rattaché à sa nouvelle tâche
                tache = Tache.objects.create(
                    titre=titre_recu,
                    description=desc_recue or '',
                    date_due=date_due_recue or None,
                    statut_en_cours=True,
                    user=request.user
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