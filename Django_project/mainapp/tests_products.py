from django.test import TestCase

from mainapp.models import Product, ProductCategory


class ProductsTestCase(TestCase):
    def setUp(self):
        category = ProductCategory.objects.create(name="Триумф")
        self.product_1 = Product.objects.create(
            name="Бонневиль", category=category, price=1999.5, quantity=13
        )
        self.product_2 = Product.objects.create(
            name="Рокет", category=category, price=1998.5, quantity=12, is_active=False
        )
        self.product_3 = Product.objects.create(
            name="Трайдент", category=category, price=1997.5, quantity=11
        )

    def test_product_get(self):
        product_1 = Product.objects.get(name="Бонневиль")
        product_2 = Product.objects.get(name="Рокет")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_print(self):
        product_1 = Product.objects.get(name="Бонневиль")
        product_2 = Product.objects.get(name="Рокет")
        self.assertEqual(str(product_1), "Бонневиль (Триумф)")
        self.assertEqual(str(product_2), "Рокет (Триумф)")

    def test_product_get_items(self):
        product_1 = Product.objects.get(name="Бонневиль")
        product_3 = Product.objects.get(name="Трайдент")
        products = Product.get_items()

        self.assertEqual(list(products), [product_1, product_3])
