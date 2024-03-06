import random
from decimal import Decimal
from pathlib import Path
from random import randint

from django.contrib.auth.models import User, Group, Permission
from django.core import management
from django.core.management.base import BaseCommand
from faker import Faker

from inventories.models import Supplier, Product, ProductImage

fake = Faker()


def generate_inventories(n=1000):
    for i in range(n // 10):
        Supplier.objects.create(
            name=fake.company(),
            contact_person=fake.name(),
            email=fake.ascii_company_email(),
            phone_number=fake.phone_number(),
            address=fake.address()
        )

    suppliers = Supplier.objects.all()

    def get_supplier(s=suppliers):
        if s.count() == 1:
            return s[0]
        else:
            return s[randint(0, s.count() - 1)]

    for _ in range(n):
        p = Product.objects.create(
            name=fake.catch_phrase(),
            description=fake.bs(),
            price=float(Decimal(random.randrange(1_000, 100_000)) / 100),
            quantity=1000,
            supplier=get_supplier()
        )

        ProductImage.objects.create(
            product=p,
            # image=
        )


class Command(BaseCommand):
    help = 'Populates Supplier and Product tables with sample data'

    def handle(self, *args, **options):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        db_path = Path.joinpath(BASE_DIR, 'db.sqlite3')
        # print(db_path)
        Path.unlink(db_path)  # delete db.sqlite3
        management.call_command('migrate')

        guest_group = Group.objects.create(name='Guest')
        view_product_permission = Permission.objects.get(codename='view_product')
        guest_group.permissions.add(view_product_permission)
        guest_user = User.objects.create_user(username='guest', email=fake.email(), password='abcdwxyz')
        guest_user.groups.add(guest_group)

        superuser = User.objects.create_superuser(username='juwaini', email=fake.email(), password='abcdwxyz')
        admin_group = Group.objects.create(name='Admin')
        admin_permission = [Permission.objects.get(codename=n) for n in
                            ('add_product', 'view_product', 'change_product', 'delete_product')]
        for a in admin_permission:
            admin_group.permissions.add(a)
        superuser.groups.add(admin_group)

        generate_inventories()
