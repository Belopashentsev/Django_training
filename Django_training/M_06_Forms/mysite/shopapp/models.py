from django.contrib.auth.models import User
from django.db import models

# функция формирования пути для хранения превью
def product_preview_directory_path(instance: "Product", filename: str) -> str:
    return "products/product_{pk}/preview/{filename}".format(pk=instance.pk, filename=filename)

class Product(models.Model):
    class Meta:
        ordering = ["name", "price"]
        # db_table = "tech_products"
        # verbose_name_plural = "products"

    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)

    created_by = models.OneToOneField(User, models.SET_NULL, null=True, blank=True)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)

    # @property
    # def description_short(self):
    #     if len(self.description) < 50:
    #         return self.description
    #     return self.description[:48] + "..."

    def __str__(self):
        return f"Product(pk={self.pk}, name={self.name!r})"

# функция формирования пути для хранения подробных изображений
def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    return "products/product_{id}/images/{filename}".format(id=instance.product.pk, filename=filename)


# класс подробных изображений, так же есть редакции в admin.py (ProductInline)
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=product_images_directory_path)
    description = models.CharField(max_length=150, null=False, blank=True)



class Order(models.Model):
    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")
    receipt = models.FileField(null=True, upload_to='orders/receipts/')
# null=True т.к есть заказы без чека,
# upload_to указывает куда загружать файлы для этого поля (старт из MEDIA_ROOT)
