import random
from decimal import Decimal
from random import randint

from django.contrib.auth.models import User, Group, Permission
from django.core.management.base import BaseCommand

from inventories.models import Supplier, Product, ProductImage

from faker import Faker

fake = Faker()


def generate_inventories(n=1000):
    for i in range(n//10):
        Supplier.objects.create(
            name=fake.company(),
            contact_person=fake.name(),
            email=fake.ascii_company_email(),
            phone_number=fake.phone_number(),
            address=fake.address()
        )

    suppliers = Supplier.objects.all()
    for _ in range(n):
        p = Product.objects.create(
            name=fake.catch_phrase(),
            description=fake.bs(),
            price=float(Decimal(random.randrange(1_000, 100_000)) / 100),
            quantity=1000,
            supplier=suppliers[randint(0, len(suppliers) - 1)]
        )

        ProductImage.objects.create(
            product=p,
            # image=
        )


class Command(BaseCommand):
    help = 'Populates Supplier and Product tables with sample data'

    def handle(self, *args, **options):
        self.guest_group = Group.objects.create(name='Guest')
        view_product_permission = Permission.objects.get(codename='view_product')
        self.guest_group.permissions.add(view_product_permission)
        self.guest_user = User.objects.create_user(username='guest', email=fake.email(), password='abcdwxyz')
        self.guest_user.groups.add(self.guest_group)

        User.objects.create_superuser(username='juwaini', email=fake.email(), password='abcdwxyz')

        generate_inventories()