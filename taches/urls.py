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


    path('api/ajouter_tache',views.api_create_tache,name='tache_creation')

]