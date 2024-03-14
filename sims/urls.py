"""
URL configuration for sims project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

from inventories.api_views import ProductViewSet, SupplierViewSet
from inventories.views import (ProductAPIView, ProductListView, ProductCreateView,
                               ProductDetailView, ProductUpdateView, ProductDeleteView, IndexView, logout_view)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('accounts/logout/', logout_view, name='logout'),

    # path('accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/accounts/login'}),

    # Product (Web)
    path('inventory/', ProductListView.as_view(), name='list-products'),
    path('create-inventory/', ProductCreateView.as_view(), name='create-product'),
    path('inventory/<int:pk>/', ProductDetailView.as_view(), name='detail-product'),
    path('update-inventory/<int:pk>', ProductUpdateView.as_view(), name='update-product'),
    path('delete-inventory/<int:pk>', ProductDeleteView.as_view(), name='delete-product'),

    # Product (API)
    path('api/inventory/', ProductViewSet.as_view({'get': 'list'}), name='api-list-products'),
    path('api/inventory/<int:pk>', ProductViewSet.as_view({'get': 'retrieve'}), name='api-detail-product'),
    path('api/add-inventory/', ProductAPIView.as_view(), name='api-create-product'),
    path('api/delete-inventory/<int:pk>', ProductAPIView.as_view(), name='api-delete-product'),
    path('api/update-inventory/<int:pk>', ProductAPIView.as_view(), name='api-update-product'),

    # Supplier (API)
    path('api/supplier', SupplierViewSet.as_view({'get': 'list'}), name='api-supplier-list'),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),

    path("__debug__/", include("debug_toolbar.urls")),
]
