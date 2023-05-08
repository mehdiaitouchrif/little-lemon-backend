from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer
from .permissions import IsManagerOrAdmin


# Categories
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


# Menu Items
class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    search_fields = ['category__title', 'title']
    ordering_fields = ['price', 'title']

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsManagerOrAdmin, IsAuthenticated]
        return [permission() for permission in permission_classes]

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsManagerOrAdmin, IsAuthenticated]
        return [permission() for permission in permission_classes]