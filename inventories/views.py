from django.http import Http404
from django.urls import reverse
from django.views.generic import ListView, TemplateView, CreateView, DetailView
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status

from inventories.forms import ProductForm
from inventories.models import Product
from inventories.serializers import ProductSerializer


class ProductListView(TemplateView):
    template_name = 'product-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all().select_related('supplier')
        context['title'] = 'Product List'
        return context


class ProductDetailView(DetailView):
    template_name = 'product-detail.html'
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('supplier')
        return queryset


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product-create.html'
    success_url = '/inventory/'  # reverse('list-products')


class ProductAPIListView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        # print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductAPIDetailView(APIView):
    # queryset = Product.objects.all()
    # serializer_class = ProductSerializer
    # lookup_field = 'pk'

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductAPICreateView(CreateAPIView):
    pass
