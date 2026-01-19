from django.contrib import admin
from .models import Category, Cours

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']

@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = [
        'nom', 'category', 'date', 'heureDebut', 'heureFin',
        'placesoccupees', 'capacite_max', 'places_disponibles', 'est_complet_display'
    ]
    list_filter = ['category', 'date']
    search_fields = ['nom']
    readonly_fields = ['places_disponibles', 'est_complet_display']

    def places_disponibles(self, obj):
        return obj.places_disponibles()
    places_disponibles.short_description = "Places disponibles"

    def est_complet_display(self, obj):
        return "Oui" if obj.est_complet() else "Non"
    est_complet_display.short_description = "Complet ?"
