from django.urls import path
from . import views

urlpatterns = [
    path('categories', views.CategoriesView.as_view()),
    path('categories/<int:pk>', views.SingleCategoryView.as_view()),
]