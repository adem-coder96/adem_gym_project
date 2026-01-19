from rest_framework import serializers
from .models import Category, Cours

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CoursSerializer(serializers.ModelSerializer):
    places_disponibles = serializers.SerializerMethodField()
    entraineur = serializers.StringRelatedField(source='id_Utilisateur')

    class Meta:
        model = Cours
        fields = '__all__'

    def get_places_disponibles(self, obj):
        return obj.places_disponibles()
