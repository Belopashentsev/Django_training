import json
from django.test import TestCase
from django.urls import reverse

class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        # используем метод get класса client, который имитирует гет запрос к URL.
        # в скобках указываем URL (в даном случае он будет сформирован функцией reverse)
        # от тестируемой функции вернется ответ,
        # содержимое которого мы проверим с помощью assertContains,
        # так же при этом будет проверен статус-код
        response = self.client.get(reverse("myauth:cookie_get"))
        self.assertContains(response, "Cookie value")
        # проверяем содержится ли в ответе искомая строка


# JSON тест содержимого "вручную"
class FooBarViewTestCase(TestCase):
    def test_foobarview(self):
        # обращаемся к вью-классу и получаем ответ,
        # проверяем сатус-код, проверяем тип содержимого
        # записываем эталонное содержимое в переменную и сравниваем его с полученным в ответе
        response = self.client.get(reverse("myauth:foo_bar"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], 'application/json')
        expected_data = {"foo": "bar", "span": "eggs"}

        # # контент в ответе приходит в байтовом (str) формате и отличается от словаря,
        # # преобразуем контент в словарь
        # received_data = json.loads(response.content)
        # self.assertEqual(received_data, expected_data)

        # используем инструмент джанго для сокращения кода:
        self.assertJSONEqual(response.content, expected_data)