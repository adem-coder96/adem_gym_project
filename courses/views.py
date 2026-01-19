from rest_framework import viewsets, permissions
from .models import Category, Cours
from .serializers import CategorySerializer, CoursSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class CoursViewSet(viewsets.ModelViewSet):
    queryset = Cours.objects.all()
    serializer_class = CoursSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Use Django's built-in permissions or custom logic
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]