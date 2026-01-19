from django.contrib import admin
from .models import Notifications

@admin.register(Notifications)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["titre", "user", "dateEnvoi", "is_read"]
    list_filter = ["is_read", "dateEnvoi"]
    search_fields = ["titre", "message", "user__username"]
    readonly_fields = ["dateEnvoi"]