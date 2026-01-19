from rest_framework import serializers
from .models import Utilisateurs


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Utilisateurs
        fields = ['username', 'email', 'password', 'tel']

    def create(self, validated_data):
        user = Utilisateurs.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            tel=validated_data['tel'],
            role='membre'
        )
        return user
