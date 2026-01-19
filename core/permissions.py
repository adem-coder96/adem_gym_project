from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        # Check if user is authenticated and has admin role
        return request.user and request.user.is_authenticated and request.user.role == 'administrateur'

class IsEntraineur(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'entraîneur'

class IsMembre(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'membre'

class IsAdminOrEntraineur(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role in ['administrateur', 'entraîneur']

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # For objects that have an id_Utilisateur field
        if hasattr(obj, 'id_Utilisateur'):
            return request.user == obj.id_Utilisateur or request.user.role == 'administrateur'
        return False