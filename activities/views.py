"""Vues pour l'application des activités."""
import urllib.request
from urllib import parse
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Category, Activity
from .forms import NewActivityForm, UserCreationForm



def index(request):
    """Vue pour la page d'accueil. Affiche toutes les activités."""

    filtre = request.GET.get('filtre', 'toutes')
    categorie_id = request.GET.get('category')

    activites_list = Activity.objects.all()

    if filtre == 'mes_proposees' and request.user.is_authenticated:
        activites_list = activites_list.filter(proposer=request.user)
    elif filtre == 'mes_inscriptions' and request.user.is_authenticated:
        activites_list = activites_list.filter(attendees=request.user)

    if categorie_id:
        activites_list = activites_list.filter(category=categorie_id)

    pagination = Paginator(activites_list, 3)
    nb_page = request.GET.get('page')
    activites = pagination.get_page(nb_page)

    categories = Category.objects.all()

    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    return render(request, 'activities/index.html', {'activites': activites, 'user': user, 'filtre': filtre, 'categories': categories, 'categorie_id': categorie_id})

def signup(request):
    """Vue pour la page d'inscription."""

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def new_activity(request):
    """Vue pour la page de création d'une activité."""

    if request.method == 'POST':
        form = NewActivityForm(request.POST, proposer=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = NewActivityForm(proposer=request.user)

    return render(request, 'activities/new_activity.html', {'form': form})

def details_activity(request, activity_id):
    """Vue pour la page de détails d'une activité."""
    activite = get_object_or_404(Activity, id=activity_id)

    if request.method == 'POST' and request.user.is_authenticated:
        if 'inscrire' in request.POST:
            activite.attendees.add(request.user)
        elif 'desinscrire' in request.POST:
            activite.attendees.remove(request.user)
        return redirect('details_activity', activity_id=activity_id)

    aqi = None
    ville = activite.location_city
    ville_encoded = parse.quote(ville)

    url = f'https://api.waqi.info/feed/{ville_encoded}/?token={settings.WAQI_API_TOKEN}'

    res = urllib.request.urlopen(url)
    data = json.loads(res.read())
    if data.get('status') == 'ok':
        aqi = data['data'].get('aqi')

    return render(request, 'activities/details_activity.html', {'activite': activite, 'aqi': aqi})

@login_required
def profile(request):
    """Vue pour la page de profil utilisateur."""
    return render(request, 'activities/profile.html', {'username': request.user.username})

@login_required
def edit_profile(request, username):
    """"Vue pour la page d'édition du profil utilisateur."""
    return render(request, 'activities/edit_profile.html', {'username': username})

def page_not_found(request, exception):
    """Vue pour la page d'erreur 404."""
    return render(request, "errors/404.html", status=404)

def server_error(request):
    """Vue pour la page d'erreur 500."""
    return render(request, "errors/500.html", status=500)