from django.urls import path
from . import views

urlpatterns = [
    path('categories', views.CategoriesView.as_view()),
    path('categories/<int:pk>', views.SingleCategoryView.as_view()),
    path('menu-items', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('cart/menu-items', views.CartView.as_view()),
]