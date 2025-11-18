from django.urls import path
from taches import views


urlpatterns = [
    path('',views.home,name='home'),
    path('liste/', views.liste_taches, name='tache'),  
    path('creer-tache/', views.tacheCreate, name='tache_creation'),

]