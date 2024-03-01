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

from inventories.views import (ProductAPIListView, ProductAPIDetailView, ProductListView, ProductCreateView,
                               ProductDetailView, ProductUpdateView, ProductDeleteView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),

    path('inventory/', ProductListView.as_view(), name='list-products'),
    path('create-inventory/', ProductCreateView.as_view(), name='create-product'),
    path('inventory/<int:pk>/', ProductDetailView.as_view(), name='detail-product'),
    path('update-inventory/<int:pk>', ProductUpdateView.as_view(), name='update-product'),
    path('delete-inventory/<int:pk>', ProductDeleteView.as_view(), name='delete-product'),

    path('api/inventory', ProductAPIListView.as_view(), name='api-list-products'),
    path('api/add-inventory/', ProductAPIListView.as_view(), name='api-create-product'),
    path('api/inventory/<int:pk>', ProductAPIDetailView.as_view(), name='api-detail-product'),
    path('api/delete-inventory/<int:pk>', ProductAPIDetailView.as_view(), name='api-delete-product'),
    path('api/update-inventory/<int:pk>', ProductAPIDetailView.as_view(), name='api-update-product'),

    path("__debug__/", include("debug_toolbar.urls")),
]
