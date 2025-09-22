"""Forms pour la gestion des activités et des utilisateurs."""

from django import forms
from django.utils import timezone
from .models import User, Activity, Category


class ModifyProfileForm(forms.ModelForm):
    """Formulaire pour la modification du profil utilisateur."""

    class Meta:
        model = User
        fields = ["avatar", "first_name", "last_name", "email", "bio"]
        widgets = {
            "avatar": forms.FileInput(
                attrs={"class": "form-control w-100", "accept": "image/*"}
            ),
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "prenom": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class NewActivityForm(forms.ModelForm):
    """Formulaire pour la création d'une nouvelle activité."""

    class Meta:
        """Meta data pour le formulaire NewActivityForm."""
        model = Activity
        fields = [
            "title",
            "description",
            "location_city",
            "start_time",
            "end_time",
            "category",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "location_city": forms.TextInput(attrs={"class": "form-control"}),
            "start_time": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "end_time": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "category": forms.Select(attrs={"class": "form-control"}),
        }


class UserCreationForm(forms.Form):
    """Formulaire pour la création d'un nouvel utilisateur."""

    username = forms.CharField(label="Nom d'utilisateur", max_length=150)
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirmer le mot de passe", widget=forms.PasswordInput
    )

    def clean_username(self):
        """Vérifie que le nom d'utilisateur est unique."""
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

        return cleaned_data

    def save(self, commit=True):
        """Crée et retourne un nouvel utilisateur."""
        user = User(username=self.cleaned_data["username"])
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
