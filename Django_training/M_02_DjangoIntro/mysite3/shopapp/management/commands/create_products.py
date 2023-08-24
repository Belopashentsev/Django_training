from django.core.management import BaseCommand
from shopapp.models import Product

class Command(BaseCommand):
    """
    Create new products
    """
    def handle(self, *args, **options):
        self.stdout.write('Create product')
        products_names = [
            'Laptop',
            'Desctop',
            'BigThing'
        ]
        for product_name in products_names:
            product, created = Product.objects.get_or_create(name=product_name)
            self.stdout.write(f'Create product: {product.name}')

        self.stdout.write(self.style.SUCCESS("Product create!"))