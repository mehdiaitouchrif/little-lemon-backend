"""
URL configuration for littlelemon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from rest_framework import routers, permissions
from littlelemonapi.views import MenuItemImageViewSet

router = routers.DefaultRouter()
router.register(r'menu-items/(?P<menu_item_pk>\d+)/images', MenuItemImageViewSet, basename='menu-item-images')

schema_view = get_schema_view(
    openapi.Info(
        title="Welcome to Little Lemon API Documentation",
        default_version='v1',
        description="""The Little Lemon Backend API is a Django-powered backend that offers a range of endpoints to manage customers, menu items, categories, orders, delivery crew users, and user groups. 
                       Users can register, login, and logout, while customers can browse the menu, add items to their cart, and place orders. Managers have full control over categories and menu items, can update orders, 
                       assign delivery crew members, and manage customer groups. Delivery crew users can easily update their assigned orders. This API provides a robust foundation for efficient operations and a seamless user experience 
                       within the Little Lemon app.""",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('littlelemonapi.urls')),
    path('api/', include(router.urls)),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('__debug__/', include('debug_toolbar.urls'))
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)