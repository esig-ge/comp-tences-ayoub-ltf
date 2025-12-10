from django.conf import settings
from django.db import models
from django.utils import timezone

class Tache(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True) # Description facultative
    date_creation = models.DateTimeField(default=timezone.now)
    date_due = models.DateTimeField(blank=True, null=True) # Date limite facultative
    statut_en_cours = models.BooleanField(default=True)


    def __str__(self):
        return self.titre
