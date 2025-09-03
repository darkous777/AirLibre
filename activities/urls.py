from django.urls import path
from . import views # Importe le fichier views depuis le dossier courant

urlpatterns = [
    path('', views.index, name='index'), # Définition de la route par défaut qui pointe vers la vue index
]