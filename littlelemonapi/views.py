from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import Category
from .serializers import CategorySerializer

class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Manager').exists())

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsManagerOrAdmin, IsAuthenticated]
        return [permission() for permission in permission_classes]

class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsManagerOrAdmin, IsAuthenticated]
        return [permission() for permission in permission_classes]