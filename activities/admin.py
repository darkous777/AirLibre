"""Configuration de l'interface d'administration pour les modèles d'activités."""
from django.contrib import admin
from .models import Category, User, Activity

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Interace pour gérer les utilisateurs dans l'admin Django."""
    list_display = ('username', 'email', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Interace pour gérer les catégories dans l'admin Django."""
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Interace pour gérer les activités dans l'admin Django."""
    list_display = ('title', 'proposer', 'category', 'start_time', 'end_time')
    search_fields = ('title', 'description', 'location_city')
    list_filter = ('category', 'start_time', 'end_time')
