from django.urls import path
from taches import views
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home,name='home'),
    path('liste/', views.liste_view, name='tache'),
    path('creer-tache/', views.tache_create, name='tache_creation'),
    path('modifier-tache/<int:pk>/', views.tache_update, name='tache_modifier'),
    path('supprimer-tache/<int:pk>/',views.tache_delete,name='tache_supprimer'),
    path('basculer-statut/<int:pk>/',views.tache_statut,name='basculer_statut'),
    path('tache/<int:pk>/', views.tache_detail, name='tache_detail'),

    # 4. API AJAX (Séparée)
    path('api/ajouter-commentaire/', views.ajouter_commentaire_ajax, name='ajouter_commentaire_ajax'),
]