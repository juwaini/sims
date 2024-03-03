from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView
from rest_framework import authentication, status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.settings import api_settings

from inventories.forms import ProductForm
from inventories.models import Product
from inventories.serializers import ProductSerializer


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


class ProductListView(PermissionRequiredMixin, TemplateView):
    permission_required = ['inventories.view_product', ]
    template_name = 'product-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all().select_related('supplier')
        context['title'] = 'Product List'
        return context


class ProductDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ['inventories.view_product', ]
    template_name = 'product-detail.html'
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('supplier')
        return queryset


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ['inventories.add_product', ]
    model = Product
    form_class = ProductForm
    template_name = 'product-create.html'
    success_url = '/inventory/'  # reverse('list-products')


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ['inventories.update_product', ]
    model = Product
    form_class = ProductForm
    template_name = 'product-update.html'

    def get_success_url(self):
        return reverse('detail-product', kwargs={'pk': self.kwargs['pk']})


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ['inventories.delete_product', ]
    model = Product
    success_url = reverse_lazy('list-products')


class ProductAPIView(APIView):
    authentication_classes = [authentication.SessionAuthentication]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        if not request.user.has_perm('inventories.add_product'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        if not request.user.has_perm('inventories.view_product'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if not request.user.has_perm('inventories.update_product'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not request.user.has_perm('inventories.delete_product'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductAPICreateView(CreateAPIView):
    pass
