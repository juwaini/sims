import json
import random
from decimal import Decimal

from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient

from .management.commands.populate_data import fake, generate_inventories
from .models import Product, Supplier

fake = Faker()


class ProductTestCase(TestCase):
    def setUp(self):
        # Create user without any permission
        self.nothing_user = User.objects.create_user(username='nothing', email=fake.email(), password=fake.password())

        # Create user with Guest permission
        self.guest_group = Group.objects.create(name='Guest')
        view_product_permission = Permission.objects.get(codename='view_product')
        self.guest_group.permissions.add(view_product_permission)
        self.guest_user = User.objects.create_user(username='guest', email=fake.email(), password=fake.password())
        self.guest_user.groups.add(self.guest_group)

        # Create superuser that can do all
        self.superuser = User.objects.create_superuser(username='superuser', email=fake.email(),
                                                       password=fake.password())
        self.admin_group = Group.objects.create(name='Admin')
        admin_permission = [Permission.objects.get(codename=n) for n in ('add_product', 'view_product', 'change_product', 'delete_product')]
        for a in admin_permission:
            self.admin_group.permissions.add(a)
        self.superuser.groups.add(self.admin_group)

    def test_api_list_inventory_for_user_with_no_permission(self):
        self.client.force_login(self.nothing_user, backend=None)
        url = reverse('api-list-products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_list_inventory_for_guest_user(self):
        generate_inventories(100)

        self.client.force_login(self.guest_user, backend=None)
        url = reverse('api-list-products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.json())
        # self.assertEqual(type(response.data), json)

    def test_api_details_inventory_for_guest_user(self):
        generate_inventories(10)

        self.client.force_login(self.guest_user, backend=None)
        url = reverse('api-detail-product', kwargs={'pk': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_create_inventory_for_guest_user(self):
        self.client.force_login(self.guest_user, backend=None)
        s = Supplier.objects.create(
            name=fake.company(),
            contact_person=fake.name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            address=fake.address()
        )
        url = reverse('api-create-product')
        product = {
            'name': fake.bs(),
            'description': fake.catch_phrase(),
            'price': Decimal(random.randrange(10, 10_000)),
            'quantity': 10_000,
            'supplier': s.pk
        }

        response = self.client.post(url, data=product)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_create_inventory_for_admin_user(self):
        self.client.force_login(self.superuser, backend=None)
        s = Supplier.objects.create(
            name=fake.company(),
            contact_person=fake.name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            address=fake.address()
        )
        url = reverse('api-create-product')
        before = Product.objects.all().count()
        product = {
            'name': fake.bs(),
            'description': fake.catch_phrase(),
            'price': Decimal(random.randrange(10, 10_000)),
            'quantity': 10_000,
            'supplier': s.pk
        }

        response = self.client.post(url, data=product)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(before + 1, Product.objects.all().count())

    #
    def test_api_delete_inventory(self):
        self.client.force_login(self.guest_user, backend=None)

        url = reverse('api-delete-product', kwargs={'pk': 1})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_update_inventory(self):
        generate_inventories(5)

        self.client.force_login(self.guest_user, backend=None)
        client = APIClient()

        s = Supplier.objects.get(pk=1)
        before = Product.objects.all().count()
        name_before = Product.objects.get(pk=1).name
        product = {
            'name': 'Product Juwaini',
            # 'description': fake.catch_phrase(),
            # 'price': Decimal(random.randrange(10, 10_000)),
            # 'quantity': 10_000,
            # 'supplier': s.pk
        }
        url = reverse('api-update-product', kwargs={'pk': 1})
        response = client.put(url, data=product)
        # print(response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        after = Product.objects.all().count()

        self.assertEqual(before, after)
        name_after = Product.objects.get(pk=1).name
