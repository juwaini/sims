import random
from decimal import Decimal
from random import randint

from django.core.management.base import BaseCommand
from inventories.models import Supplier, Product, ProductImage

from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Populates Supplier and Product tables with sample data'

    def handle(self, *args, **options):
        for i in range(100):
            Supplier.objects.create(
                name=fake.company(),
                contact_person=fake.name(),
                email=fake.ascii_company_email(),
                phone_number=fake.phone_number(),
                address=fake.address()
            )

        suppliers = Supplier.objects.all()
        for _ in range(1000):
            p = Product.objects.create(
                name=fake.catch_phrase(),
                description=fake.bs(),
                price=Decimal(random.randrange(10, 1000)),
                quantity=1000,
                supplier=suppliers[randint(0, len(suppliers) - 1)]
            )

            ProductImage.objects.create(
                product=p,
                # image=
            )