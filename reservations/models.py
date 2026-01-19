from django.db import models
from users.models import Utilisateurs
from courses.models import Cours


class Reservation(models.Model):
    RESERVATION_STATUT = [
        ('confirmée', 'Confirmée'),
        ('en_attente', 'En Attente'),
        ('annulée', 'Annulée'),
    ]

    dateReservation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=20,
        choices=RESERVATION_STATUT,
        default='en_attente'
    )
    present = models.BooleanField(default=False)

    # Make this nullable first, then we'll update it
    id_Utilisateur = models.ForeignKey(
        Utilisateurs,
        on_delete=models.CASCADE,
        related_name='reservations',
        null=True,  # ADD THIS
        blank=True  # ADD THIS
    )
    id_Cour = models.ForeignKey(
        Cours,
        on_delete=models.CASCADE,
        related_name='reservations'
    )

    class Meta:
        verbose_name_plural = "Reservations"
        unique_together = ['id_Utilisateur', 'id_Cour']

    def __str__(self):
        return f"Réservation {self.id} - {self.id_Utilisateur.username if self.id_Utilisateur else 'No User'} - {self.id_Cour.nom}"