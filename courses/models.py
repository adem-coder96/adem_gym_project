from django.db import models
from users.models import Utilisateurs


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Cours(models.Model):
    nom = models.CharField(max_length=200)
    date = models.DateField()
    heureDebut = models.TimeField()
    heureFin = models.TimeField()
    placesoccupees = models.IntegerField(default=0)
    capacite_max = models.IntegerField(default=20)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="cours"
    )

    # Add the missing ForeignKey
    id_Utilisateur = models.ForeignKey(
        Utilisateurs,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cours"
    )

    def __str__(self):
        return self.nom

    def places_disponibles(self):
        return self.capacite_max - self.placesoccupees

    def est_complet(self):
        return self.placesoccupees >= self.capacite_max

    class Meta:
        verbose_name_plural = "Cours"