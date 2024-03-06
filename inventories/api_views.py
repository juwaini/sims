from rest_framework import viewsets, status, mixins, pagination, authentication
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from inventories.models import Product, Supplier
from inventories.serializers import ProductSerializer, SupplierSerializer


class SupplierViewSet(ModelViewSet):
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    queryset = Supplier.objects.all().order_by('id')

    def list(self, request, *args, **kwargs):
        pag = self.paginate_queryset(self.queryset)
        serializer = SupplierSerializer(pag, many=True)
        return self.get_paginated_response(serializer.data)


class ProductViewSet(ModelViewSet):
    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.SessionAuthentication
    )
    queryset = Product.objects.all().order_by('id')

    def list(self, request, *args, **kwargs):
        if not request.user.has_perm('inventories.view_product'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        # queryset = Product.objects.all()
        pagination_result = self.paginate_queryset(self.queryset)
        serializer = ProductSerializer(pagination_result, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, *arg, **kwargs):
        if not request.user.has_perm('inventories.view_product'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=kwargs.get('pk'))
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm('inventories.add_product'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
