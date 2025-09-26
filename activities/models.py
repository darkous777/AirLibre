"""Modèles pour l'application des activités."""

from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.forms import ValidationError
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Modèle représentant un utilisateur de l'application."""

    avatar = models.ImageField(upload_to='avatar/', blank=True)
    bio = models.TextField(max_length=500, blank=True)

    class Meta:
        """Meta data pour le modèle User."""

        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ["username"]

    def __str__(self):
        return f"{self.username}"


class Category(models.Model):
    """Modèle représentant une catégorie d'activités."""
    objects = models.Manager()
    name = models.CharField(
        verbose_name="Nom de la catégorie",
        unique=True,
        null=False,
        blank=False,
        validators=[MaxLengthValidator(100)],
    )

    class Meta:
        """Meta data pour le modèle Category."""

        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["name"]

    def clean(self):
        super().clean()

        if len(self.name) > 100:
            raise ValidationError("Le nom de la catégorie ne peut pas dépasser 100 caractères.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Activity(models.Model):
    """Modèle représentant une activité proposée par un utilisateur."""
    objects = models.Manager()
    title = models.CharField(
        verbose_name="Titre",
        null=False,
        blank=False,
        validators=[MinLengthValidator(5), MaxLengthValidator(200)],
    )
    description = models.TextField(
        verbose_name="Description",
        null=False,
        blank=False,
        validators=[MinLengthValidator(10)],
    )
    location_city = models.CharField(
        verbose_name="Ville",
        null=False,
        blank=False,
        validators=[MinLengthValidator(2), MaxLengthValidator(100)],
    )
    start_time = models.DateTimeField(
        verbose_name="Date et heure de début",
        null=False,
        blank=False,
    )
    end_time = models.DateTimeField(
        verbose_name="Date et heure de fin",
        null=False,
        blank=False,
    )
    proposer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="proposed_activities"
    )
    attendees = models.ManyToManyField(
        User, related_name="attended_activities", verbose_name="Participants"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activities",
        verbose_name="Catégorie",
    )

    class Meta:
        """Meta data pour le modèle Activity."""

        verbose_name = "Activité"
        verbose_name_plural = "Activités"
        ordering = ["start_time"]

    def clean(self):
        """Validation personnalisée pour s'assurer que la date de début est dans le futur
        et que la date de fin est après la date de début."""

        if self.start_time is None or self.end_time is None:
            raise ValidationError("Les dates de début et de fin doivent être renseignées.")

        if self.start_time <= timezone.now():
            raise ValidationError("La date de début doit être dans le futur.")

        if self.end_time <= self.start_time:
            raise ValidationError(
                "La date de fin doit être postérieure à la date de début."
            )

        if len(self.title) < 5 or len(self.title) > 200:
            raise ValidationError("Le titre doit contenir entre 5 et 200 caractères.")

        if len(self.description) < 10:
            raise ValidationError("La description doit contenir au moins 10 caractères.")

        if len(self.location_city) < 2 or len(self.location_city) > 100:
            raise ValidationError("La ville doit contenir entre 2 et 100 caractères.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"
