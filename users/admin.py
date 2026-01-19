from django.contrib import admin
from .models import Utilisateurs


@admin.register(Utilisateurs)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')
