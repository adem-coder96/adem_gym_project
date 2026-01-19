from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    utilisateur = serializers.StringRelatedField(source='id_Utilisateur', read_only=True)
    cours = serializers.StringRelatedField(source='id_Cour', read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'
