from django.urls import path

from taches import views
from taches.views import TacheCreateView, TacheUpdateView, TacheDeleteView, TacheListView


urlpatterns = [
    path('',views.home,name='home'),
    path('new/', TacheCreateView.as_view(), name='tache_create'),

    # R (Lire - Liste) : Ceci est maintenant la vue principale de liste
    path('', TacheListView.as_view(), name='liste_taches'),

    # U (Mettre à jour)
    path('<int:pk>/edit/', TacheUpdateView.as_view(), name='tache_update'),

    # D (Supprimer)
    path('<int:pk>/delete/', TacheDeleteView.as_view(), name='tache_delete'),
]