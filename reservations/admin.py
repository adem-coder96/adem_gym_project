from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'id_Utilisateur',
        'id_Cour',
        'dateReservation',
        'statut',
        'present'
    ]
    list_filter = ['statut', 'present', 'dateReservation']
    search_fields = [
        'id_Utilisateur__username',
        'id_Cour__nom'
    ]
