from django.urls import path
from .views import shopindex, groups_list, products_list, orders_list, create_product, create_order

app_name = 'shopapp'

urlpatterns = [
    path("", shopindex, name='index'),
    path("groups/", groups_list, name='groups_list'),
    path("products/", products_list, name='products_list'),
    path('orders/', orders_list, name='orders_list'),
    path('products/create/', create_product, name='product_create'),
    path('orders/create/', create_order, name='order_create')

]