from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from .models import Product, Order
from .admin_mixins import ExportAsCSVMixin


# для отображения заказов в карточке продукта:
class Orderinline(admin.TabularInline):
    model = Product.orders.through


# для архивации нескольких записей разом:
@admin.action(description='Archived(...ated) products') # чтобы функция попала в меню actions:
def mark_archivated(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archivated=True)


# для разархивации нескольких записей разом:
@admin.action(description='Unarchived(...ated) products') # чтобы функция попала в меню actions:
def mark_unarchivated(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archivated=False)

# создаем модель отображения на сайте:
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [mark_archivated, mark_unarchivated, 'export_csv'] # привязка действия к админке
    inlines = [Orderinline]
    list_display = 'pk', 'name', 'description_short', 'price', 'discount', 'archivated'# перечисляем поля, которые отобразятся на странице:
    list_display_links = 'pk', 'name' # перечислим поля, в которых будут ссылк на продукты (по умолчанию это уникальный ключ):
    ordering = 'pk', # для сортировки записей укажем поле (или поля для множественной) и "-" для инверсии (не забыть ","):
    search_fields = 'name', 'description' # для создания строки поиска (перечисляем поля, в которых ищем совпадения):
    fieldsets = [
        (None, {
            'fields': ('name', 'description'),
        }),
        ('Price_options', {
            'fields': ('price', 'discount'),
            'classes': ('wide', 'collapse',), # для расширения и сворачивания секции
        }),
        ('Extra_options', {
            'fields': ('archivated',),
            'classes': ('collapse',),
            'description': 'Extra options. Field "Archivated" is for soft delete.'
        })
    ] # для группировки и настройки полей в карточке продукта.

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 40:
            return obj.description
        return obj.description[:40] + '...'
admin.site.register(Product, ProductAdmin) # регистрируем импортированную модель Продукт и модель её отображения в административной панели сайта:


# альтернативное создание модели отображения с помощью декоратора:
# @admin.site.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = 'pk', 'name', 'description', 'price', 'discount'
#     list_display_links = 'pk', 'name'


# для отображения продуктов в карточке заказа:
class Productinline(admin.StackedInline): # можно использовать TabularInline, отличие в верстке.

    model = Order.products.through # укажем модель для отображения данных.
                                   # Through указывает, что выводим только те продукты, что есть в заказе.


@admin.register(Order) # Указываем, что данная модель создана для отображения заказов.
class OrderAdmin(admin.ModelAdmin):
    inlines = [Productinline] # будет отображаться в карточке заказа.
    list_display = 'delivery_adress', 'promocode', 'created_at', 'user_verbose'

    # для оптимизации запросов создадим метод, он позволи не запрашивать данные о пользователе для каждой записи,
    # а получать информацю о пользователях за один запрос:
    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')

    # для отображения имени пользователя при его доступности (имени) создадим метод:
    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username



