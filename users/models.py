from django.db import models
from django.contrib.auth.models import AbstractUser


class RoleType(models.TextChoices):
    ADMIN = 'admin', 'Administrateur'
    ENTRAINEUR = 'entraineur', 'Entraîneur'
    MEMBRE = 'membre', 'Membre'


class Utilisateurs(AbstractUser):
    tel = models.CharField(max_length=20)
    role = models.CharField(
        max_length=20,
        choices=RoleType.choices,
        default=RoleType.MEMBRE
    )

    def __str__(self):
        return self.username
