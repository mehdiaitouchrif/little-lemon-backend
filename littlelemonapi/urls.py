from django.urls import path
from . import views

urlpatterns = [
    path('categories', views.CategoriesView.as_view()),
    path('categories/<int:pk>', views.SingleCategoryView.as_view()),
    path('menu-items', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    # path('menu-items/<int:menu_item_pk>/images/', views.MenuItemImageView.as_view(), name='menu-item-images'),
    # path('menu-items/<int:menu_item_pk>/images/<int:pk>/', views.MenuItemImageView.as_view(), name='menu-item-image'),
    path('cart/menu-items', views.CartView.as_view()),
    path('orders', views.OrderView.as_view()),
    path('orders/<int:pk>', views.SingleOrderView.as_view()),
    path('reservations', views.ReservationListCreateView.as_view()),
    path('reservations/<int:pk>', views.ReservationUpdateView.as_view()),
    path('groups/manager/users', views.ManagerViewSet.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'})),
    path('groups/delivery-crew/users', views.DeliveryCrewViewSet.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'}))
]