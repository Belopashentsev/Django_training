from django.conf import settings
from string import ascii_letters
from random import choices

from django.contrib.auth.models import User, Permission
from django.test import TestCase
from .utils import add_two_numbers
from django.urls import reverse
from .models import Product, Order


# создадим класс-тест для функции utils.add_two_numbers
class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3) # вызовем тестируемую функцию и запишем результат в переменную
        self.assertEqual(result, 5) # сравним полученный результат с ожидаемым


class ProductCreateViewTestCase(TestCase):
    # сделаем предварительную настройку перед тестом
    def setUp(self) -> None:
        self.product_name = "".join(choices(ascii_letters, k=10)) # создадим рандомное имя
        Product.objects.filter(name=self.product_name).delete() # удалим одноименные сущности

    # протестируем создание продукта
    def test_product_create(self):
        # передадим client.post URL на который направится запрос и тело,
        # содержащее поля модели Product со значениями
        response = self.client.post(
            reverse("shopapp:product_create"),
            {"name": self.product_name, "price": "123.45", "description": "New table", "discount": "10"}
        )
        # согласно тестиремому вью классу вернуться должен редирект,
        # потому проверим на соответствие редиректу (и корректность статус-кода)
        self.assertRedirects(response, reverse("shopapp:products_list"))

        # убедимся, что подукт был создан
        self.assertTrue(Product.objects.filter(name=self.product_name).exists())


# тест проверки получения страницы с продуктом
class ProductDetailsViewTestCase(TestCase):
    # сделаем предварительную настройку перед тестом
    @classmethod
    def setUpClass(cls) -> None:
        cls.product_name = "".join(choices(ascii_letters, k=10)) # создадим случайное имя
        cls.product = Product.objects.create(name=cls.product_name) # создадим объект с рандомным именем

    # удалим сущность из базы после теста
    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    # отправим гет запрос на страницу, так же передадим pk как этого требует URL
    def test_get_product(self):
        response = self.client.get(
            reverse("shopapp:product_detail", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse("shopapp:product_detail", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)

# использование классов для создания и удаления сущностей позволяет не создавать их для каждого теста,
# classmethod привязывает метод ко всему классу, а не к экземпляру
# а использовать одну и ту же сущность для группы тестов
# простые setUp и tearDown выполняются перед и после КАЖДОГО теста.
# Это полезно, когда есть вероятность изменения сущности в рамках отдельного теста
# и в следующем тесте необходима заново настренная модель

# можно выгрузить все данные из базы командой "python manage.py dumpdata shopapp.Product" в консоль
# или в файл: "python manage.py dumpdata shopapp > shopapp-fixtures.json"


# тест с исп. фикстур
class ProductsListTestCase(TestCase):
    # укажем какие фикстуры использовать (будут перед каждым тестом накатываться автоматически)
    fixtures = [ "product-fixtures.json", ]

    def test_products(self):
        # # проверим данные из контекста ответа (их собирает вью класс),
        # # сравнив их с теми, что хранятся в базе
        response = self.client.get(reverse("shopapp:products_list"))
        # products = Product.objects.filter(archived=False).all() # подготовим список продуктов из базы
        # products_ = response.context["products"] # подготовим список продуктов из контекста
        # for p, p_ in zip(products, products_): # пробежимся в цикле и сравним попарно
        #     self.assertEqual(p.pk, p_.pk)

        # то же самое, но с использованием инструмента
        self.assertQuerySetEqual(
            qs=Product.objects.filter(archived=False).all(), # передаем QuerySet (ожидаемые данные)
            values= (p.pk for p in response.context["products"]), # получаемые данные для сравнения (генератор)
            transform=lambda p: p.pk # указываем как преобразовать данные из QuerySet
        )

        self.assertTemplateUsed(response, 'shopapp/products-list.html') # проверим какой шаблон был использован


# проверим аутетнификацию и авторизацию (проверим доступ)
class OrdersListViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="Bob-test", password="qqqq")# создадим нового пользователя

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    # введем логин и пароль
    def setUp(self) -> None:
        # self.client.login(**self.credentials) требует создания атрибута с логином и паролем
        self.client.force_login(self.user) # принудительный вход от имени пользователя

    # setUp и tearDown (классы в т.ч.) выполняются автоматически,
    # то есть перед тестом будет создан пользователь и выполнен вход
    def test_orders_list(self):
        response = self.client.get(reverse("shopapp:orders_list"), )
        # для проверки статус-кода и доступа проверим наличие строки Orders в ответе
        self.assertContains(response, "Orders")

    # если нужно проверить не залогиненного пользователя, то можно перенести вход или в тест функцию,
    # или сделать отдельную функцию, где пред проверкой будет произведен логаут

    def test_orders_view_not_auth(self):
        self.client.logout() # выходим
        response = self.client.get(reverse("shopapp:orders_list")) # делаем запрос и сохраняем ответ
        self.assertEqual(response.status_code, 302) # проверяем код
        self.assertIn(str(settings.LOGIN_URL), response.url) # проверяем корректность перенаправления

# 1: создаем тест и задаем поведение функции,
# далее в views прописываем функцию на основе теста
class ProductsExportViewTestCase(TestCase):
    fixtures = ["product-fixtures.json", ]

    def test_get_products_view(self):
        response = self.client.get(reverse("shopapp:products_export")) # делаем запрос и сохраняем ответ
        self.assertEqual(response.status_code, 200) # проверяем статус-код
        products = Product.objects.order_by('pk').all() # передаем QuerySet (ожидаемые данные)
        expected_data = [
            {'pk': product.pk, 'name': product.name, 'price': str(product.price), 'archived': product.archived}
            for product in products
            ] # заполняем список с ожидаемыми данными
        products_data = response.json() # получаем json тело ответа
        self.assertEqual(products_data['products'], expected_data) # сравниваем

# при первом запуске теста мы получим ошибку об отсутствии шаблона. Далее следует устранить её,
# перезапустить тест и проработать со следующей ошибкой. Таким образом повоторяем до успешного прохождения теста.


# __________homework m10__________
class OrderDetailViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='test', password='qwerty')
        permission_order = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission_order)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            delivery_address='Any street 000',
            promocode='PROMO123',
            user=self.user
            )

    def tearDown(self) -> None:
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(reverse(
            'shopapp:order_detail',
            kwargs={'pk': self.order.pk})
        )
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(response.context['order'].pk, self.order.pk)


class OrdersExportTestCase(TestCase):
    fixtures = ["order-fixtures.json", "user-fixtures.json", "products-fixtures.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass() # для корректной передачи фикстур
        cls.user = User.objects.create_user(username='test', password='qwerty')
        cls.user.is_staff = True
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_order_export_view(self):
        response = self.client.get(reverse("shopapp:orders_export"))
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by('pk').all()
        expected_data = [
            {'pk': order.pk, 'delivery_address': order.delivery_address,
             'promocode': order.promocode, 'user_id': order.user_id }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(orders_data['orders'], expected_data)
