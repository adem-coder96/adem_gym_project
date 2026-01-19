from rest_framework import viewsets, permissions
from .models import Category, Cours
from .serializers import CategorySerializer, CoursSerializer
from core.permissions import IsAdmin, IsEntraineur  # Use core permissions

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]  # Only admin can modify categories
        return [permissions.IsAuthenticated()]

class CoursViewSet(viewsets.ModelViewSet):
    queryset = Cours.objects.all()
    serializer_class = CoursSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only admin or trainer can modify courses
            return [IsAdmin() | IsEntraineur()]
        return [permissions.IsAuthenticated()]