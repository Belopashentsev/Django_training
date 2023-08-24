from django.urls import path
import mainapp.views as mainapp

# обязательно добавить
app_name = "mainapp"

urlpatterns = [
    path("", mainapp.index, name="index"),
    path("catalog/", mainapp.catalog, name="catalog"),
    path("category/<int:pk>/catalog/", mainapp.category, name="category"),
    path(
        "category/<int:pk>/catalog/page/<int:page>/",
        mainapp.category,
        name="category_page",
    ),
    path("product/<int:pk>/", mainapp.product_page, name="product_page"),
    path("contacts/", mainapp.contacts, name="contacts"),
    path("product/<int:pk>/price/", mainapp.product_price),
]
