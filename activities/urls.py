"""Fichier gérant les URL de l'application activites"""

from django.urls import path
from . import views  # Importe le fichier views depuis le dossier courant

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path(
        "activity/<int:activity_id>/", views.details_activity, name="details_activity"
    ),
    path("activity/new/", views.new_activity, name="new_activity"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
]
