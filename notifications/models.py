from django.db import models
from django.conf import settings


class Notifications(models.Model):
    titre = models.CharField(max_length=100)
    message = models.TextField()
    dateEnvoi = models.DateTimeField(auto_now_add=True)

    # Optional: Add user relationship if you want to track who receives notifications
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )

    is_read = models.BooleanField(default=False)  # Optional: track read status

    def __str__(self):
        return f"{self.titre} - {self.dateEnvoi.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name_plural = "Notifications"
        ordering = ["-dateEnvoi"]