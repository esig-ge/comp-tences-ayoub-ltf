from django.conf import settings
from django.db import models
from django.utils import timezone

class Tache(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True) # Description facultative
    date_creation = models.DateTimeField(default=timezone.now)
    date_due = models.DateTimeField(blank=True, null=True) # Date limite facultative
    completee = models.BooleanField(default=False) # L'état de la tâche
    statut_en_cours = models.BooleanField(default=True)

    def marquer_completee(self):
        self.completee = True
        self.save()

    def __str__(self):
        # Permet d'afficher le titre de la tâche dans l'interface d'administration
        return self.titre


class Commentaire(models.Model):
    # Ce champ crée le lien : Un commentaire appartient à une Tache
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)

    contenu = models.TextField()
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Commentaire sur {self.tache.titre}"