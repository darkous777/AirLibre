"""Vues pour l'application des activités."""

import urllib.request
from urllib import parse
import json
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Category, Activity, User
from .forms import NewActivityForm, UserCreationForm, ModifyProfileForm


def api_aqi(ville: str):
    """Fonction retournant la valeur AQI d'une ville avec une API."""
    try:
        ville_encoded = parse.quote(ville)

        url = f"https://api.waqi.info/feed/{ville_encoded}/?token={settings.WAQI_API_TOKEN}"

        res = urllib.request.urlopen(url)
        data = json.loads(res.read())
        if data.get("status") == "ok":
            return data["data"].get("aqi")
    except Exception:
        return None

    return None


def index(request):
    """Vue pour la page d'accueil. Affiche toutes les activités."""

    filtre = request.GET.get("filtre", "toutes")
    categorie_id = request.GET.get("category")

    activites_list = Activity.objects.all()

    if filtre == "mes_proposees" and request.user.is_authenticated:
        activites_list = activites_list.filter(proposer=request.user)
    elif filtre == "mes_inscriptions" and request.user.is_authenticated:
        activites_list = activites_list.filter(attendees=request.user)

    if categorie_id:
        activites_list = activites_list.filter(category=categorie_id)

    pagination = Paginator(activites_list, 3)
    nb_page = request.GET.get("page")
    activites = pagination.get_page(nb_page)

    categories = Category.objects.all()
    category_selected = None
    if categorie_id:
        category_selected = Category.objects.filter(id=categorie_id).first()

    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    return render(
        request,
        "activities/index.html",
        {
            "activites": activites,
            "user": user,
            "filtre": filtre,
            "categories": categories,
            "category_selected": category_selected,
        },
    )


def signup(request):
    """Vue pour la page d'inscription."""

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Inscription réussie! Vous pouvez maintenant vous connecter.",
            )
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def new_activity(request):
    """Vue pour la page de création d'une activité."""

    if request.method == "POST":
        form = NewActivityForm(request.POST)
        if form.is_valid():
            activite = form.save(commit=False)
            activite.proposer = request.user
            activite.save()
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "Activité créée avec succès!"
            )
            return redirect("index")
    else:
        form = NewActivityForm()

    return render(request, "activities/new_activity.html", {"form": form})


def details_activity(request, activity_id):
    """Vue pour la page de détails d'une activité."""
    activite = get_object_or_404(Activity, id=activity_id)

    if (
        activite.proposer == request.user
        and ("inscrire" or "desinscrire") in request.POST
    ):
        return redirect("details_activity", activity_id=activity_id)

    if request.method == "POST" and request.user.is_authenticated:
        if "inscrire" in request.POST:
            activite.attendees.add(request.user)
            activite.save()
            messages.add_message(
                request, messages.SUCCESS, "Inscription réussie à l'activité!"
            )
        elif "desinscrire" in request.POST:
            activite.attendees.remove(request.user)
            activite.save()
            messages.add_message(
                request, messages.SUCCESS, "Désinscription réussie de l'activité!"
            )
        return redirect("details_activity", activity_id=activity_id)

    aqi = api_aqi(activite.location_city)

    return render(
        request, "activities/details_activity.html", {"activite": activite, "aqi": aqi}
    )


def profile(request):
    """Vue pour la page de profil utilisateur."""

    user = get_object_or_404(User, username=request.GET.get("username"))

    if user.is_superuser:
        return redirect("index")

    return render(
        request,
        "profile/profile.html",
        {
            "user": request.user,
            "profile_user": user,
            "liste_proposer_activites": Activity.objects.filter(proposer=user),
            "liste_participer_activites": Activity.objects.filter(attendees=user),
        },
    )


@login_required
def edit_profile(request):
    """ "Vue pour la page d'édition du profil utilisateur."""
    if request.method == "POST":
        form = ModifyProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "Profil mis à jour avec succès !"
            )
            return redirect(f"/profile/?username={request.user.username}")
        else:
            messages.add_message(
                request,
                messages.ERROR,
                "Veuillez corriger les erreurs dans le formulaire.",
            )
    else:
        form = ModifyProfileForm(instance=request.user)
    return render(
        request, "profile/edit_profile.html", {"form": form, "user": request.user}
    )
