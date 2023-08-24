from django.urls import path

from .views import (
    ShopIndexView,
    GroupsListView,
    ProductDetailView,
    ProductListView,
    OrdersListView,
    OrderDetailViev,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    ProductsExportView, OrdersExportView
)

app_name = "shopapp"

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"), # as_view() преобразует класс в функцию

    # ____________________for groups____________________
    path("groups/", GroupsListView.as_view(), name="groups_list"),

    # ____________________for products____________________
    path("products/", ProductListView.as_view(), name="products_list"),
    path("products/export/", ProductsExportView.as_view(), name="products_export"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    # pk указан что бы ссылка была динамической (это диктует функция),
    # int:pk проверяет что бы pk был именно целочисленным
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archived/", ProductDeleteView.as_view(), name="product_delete"),

    # ____________________for orders____________________
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/export/", OrdersExportView.as_view(), name="orders_export"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:pk>/", OrderDetailViev.as_view(), name="order_detail"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete")


]
