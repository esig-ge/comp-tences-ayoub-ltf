from django.contrib import admin
from django.urls import path

from taches import views
urlpatterns = [
    path('',views.home,name='home'),
    path('taches', views.liste_taches, name='liste_taches'),  # Lien vers la fonction liste_taches

]