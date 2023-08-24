from timeit import default_timer

from django.contrib.auth.models import Group
from django.http import HttpRequest
from django.shortcuts import render, redirect

from .forms import ProductForm, OrderForm
from .models import Product, Order


def shopindex(request: HttpRequest):
    products = [
        ('Laptop', 500),
        ('Phone', 1000),
        ('Thing', 100500),
    ]
    context = {
        'time_running': default_timer(),
        'products': products,
    }
    return render(request, 'shopapp/shop_index.html', context=context)


def groups_list(request: HttpRequest):
    context = {
        "groups": Group.objects.prefetch_related('permissions').all()

    }
    return render(request, 'shopapp/groups_list.html', context=context)


def products_list(request: HttpRequest):
    context = {"products": Product.objects.all(),

               }
    return render(request, 'shopapp/products_list.html', context=context)


def create_product(request: HttpRequest):
    # если метод POST (отправили данные), то произвести перенаправление на страницу shopapp:products_list
    if request.method == "POST":
        form = ProductForm(request.POST)  # создаем объект-форму, предзаполненную данными из запроса
        if form.is_valid():  # проверяем валидность данных экземпляра методом класса ProductForm
            # form.cleaned_data - возвращает словарь, если ключи отличаются от ожидаемых, то можно получить
            # их отдельно и передать в Product.objects.create. (name = form.cleaned_data[name])
            # Если ключи совпадают, то можно сразу распаковать словарь в Product.objects.create(тут)
            # Product.objects.create(**form.cleaned_data) - актуально при ручном создании формы
            form.save()
            url = 'shopapp:products_list'
            return redirect(url)
    else:
        form = ProductForm()
    context = {'form': form}
    return render(request, 'shopapp/create_product.html', context=context)


def orders_list(request: HttpRequest):
    context = {
        'orders': Order.objects.select_related('user').prefetch_related('products').all()
    }
    return render(request, 'shopapp/orders_list.html', context=context)


def create_order(request: HttpRequest):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            url = 'shopapp:orders_list'
            return redirect(url)
    else:
        form = OrderForm()
    context = {'form': form}
    return render(request, 'shopapp/create_order.html', context=context)
