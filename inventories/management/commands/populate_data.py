import random
from decimal import Decimal
from random import randint

from django.contrib.auth.models import User, Group
from django.core.management.base import BaseCommand
from inventories.models import Supplier, Product, ProductImage

from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = 'Populates Supplier and Product tables with sample data'

    def handle(self, *args, **options):
        guest_user = User.objects.create_user(username='guest_user', email=fake.email(), password='abcd1234')
        guest_group = Group.objects.create(name='Guest')
        guest_user.groups.add(guest_group)

        for i in range(100):
            Supplier.objects.create(
                name=fake.company(),
                contact_person=fake.name(),
                email=fake.ascii_company_email(),
                phone_number=fake.phone_number(),
                address=fake.address()
            )

        suppliers = Supplier.objects.all()
        for _ in range(1_000):
            p = Product.objects.create(
                name=fake.catch_phrase(),
                description=fake.bs(),
                price=float(Decimal(random.randrange(1_000, 100_000))/100),
                quantity=1000,
                supplier=suppliers[randint(0, len(suppliers) - 1)]
            )

            ProductImage.objects.create(
                product=p,
                # image=
            )
