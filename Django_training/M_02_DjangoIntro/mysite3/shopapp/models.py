from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    objects = None

    class Meta:  # метакласс для определения конфигурации таблицы в целом
        ordering = ['-name', 'price']  # сортировка по имени, по убыванию
            # (раcпростарняется так же на обращения к таблице).
            # Можно указать несколько сортировок: Например тут сначала по имени, а одноименные по цене.
        # db_table = 'tech_products' # переопределение имени таблицы
        verbose_name_plural = 'products'  # указали как пишется название таблицы во мн. числе.
            # Полезно, если не решается добавлением "s".

    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archivated = models.BooleanField(default=False)

    # для корректного представления названия объекта на странице:
    def __str__(self):
        return f"Product(pk={self.pk}, name={self.name!r})" # !r - для отображения имени в кавычках.


    # для короткого отображения описания на странице:
    # @property
    # def description_short(self):
    #     if len(self.description) < 40:
    #         return self.description
    #     return self.description[:40] + '...'


class Order(models.Model):
    delivery_adress = models.TextField(null=False, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')
