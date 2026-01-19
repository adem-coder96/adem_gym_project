from rest_framework import serializers
from .models import Notifications


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Notifications
        fields = ["id", "titre", "message", "dateEnvoi", "user", "is_read"]
        read_only_fields = ["dateEnvoi", "user"]