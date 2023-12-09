from django.urls import path
from . import views
from .authentication import authentication
from littlelemonapi.authentication.refresh import CustomTokenRefreshView


urlpatterns = [
    path('categories', views.CategoriesView.as_view()),
    path('categories/<int:pk>', views.SingleCategoryView.as_view()),
    path('menu-items', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('cart/menu-items', views.CartView.as_view()),
    path('orders', views.OrderView.as_view()),
    path('orders/<int:pk>', views.SingleOrderView.as_view()),
    path('reservations', views.ReservationListCreateView.as_view()),
    path('reservations/<int:pk>', views.ReservationUpdateView.as_view()),
    path('groups/manager/users', views.ManagerViewSet.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'})),
    path('groups/delivery-crew/users', views.DeliveryCrewViewSet.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'})),
    path('auth/register', authentication.UserRegisterView.as_view(), name='register_user'),
    path('auth/login', authentication.UserLoginView.as_view(), name='user_login'),
    path('auth/profile', authentication.UserProfileView.as_view(), name='get_user_profile'),
    path('auth/logout', authentication.UserLogoutView.as_view(), name='user_logout'),
    path('auth/token/refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),
]