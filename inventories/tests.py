import random
from decimal import Decimal

from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient

from .management.commands.populate_data import fake
from .models import Product, Supplier

fake = Faker()


class ProductTestCase(TestCase):
    def setUp(self):
        self.guest_group = Group.objects.create(name='Guest')
        # permissions = Permission.objects.all()
        self.guest_user = User.objects.create_user(username='guest', email=fake.email(), password=fake.password())
        self.guest_user.groups.add(self.guest_group)

        s = Supplier.objects.create(
            name=fake.company(),
            contact_person=fake.name(),
            email=fake.ascii_company_email(),
            phone_number=fake.phone_number(),
            address=fake.address()
        )
        Product.objects.create(
            name=fake.catch_phrase(),
            description=fake.bs(),
            price=Decimal(random.randrange(10, 1000)),
            quantity=1000,
            supplier=s
        )

    def test_api_list_inventory(self):
        # self.client.force_login(self.guest_user, backend=None)
        url = reverse('api-list-products')
        products_total = Product.objects.all().count()
        response = self.client.get(url)
        # print(response.data)
        self.assertEqual(products_total, len(response.data))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_create_inventory(self):
        # self.client.force_login(self.guest_user, backend=None)
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

        response = self.client.post(url, data=product, format='')
        print(response.data)
        after = Product.objects.all().count()

        self.assertEqual(before + 1, after)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_details_inventory(self):
        url = reverse('api-detail-product', kwargs={'pk': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_delete_inventory(self):
        before = Product.objects.all().count()

        url = reverse('api-delete-product', kwargs={'pk': 1})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        after = Product.objects.all().count()
        self.assertEqual(before - 1, after)

    def test_api_update_inventory(self):
        client = APIClient()
        s = Supplier.objects.get(pk=1)
        before = Product.objects.all().count()
        name_before = Product.objects.get(pk=1).name
        product = {
            'name': 'Product Juwaini',
            'description': fake.catch_phrase(),
            'price': Decimal(random.randrange(10, 10_000)),
            'quantity': 10_000,
            'supplier': s.pk
        }
        url = reverse('api-update-product', kwargs={'pk': 1})
        response = client.put(url, data=product)
        # print(response)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        after = Product.objects.all().count()

        self.assertEqual(before, after)
        name_after = Product.objects.get(pk=1).name
        self.assertNotEqual(name_before, name_after)
        self.assertEqual('Product Juwaini', name_after)
