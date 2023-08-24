from timeit import default_timer

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group, User
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Product, Order, ProductImage
from .forms import GroupForm, ProductForm
from django.views import View


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:  # для обработки GET запроса
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
        }
        return render(request, 'shopapp/shop-index.html', context=context)


# ________________________From Groups:________________________


class GroupsListView(View):
    def get(self, request: HttpRequest):  # для обработки GET запроса
        context = {
            "form": GroupForm,
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):  # для обработки POST запроса
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)  # рендер может позволить задублировать форму, что не желательно.
        # При редиректе форма в запросе не сохраняется.


# ________________________From Products:________________________


# создадим описание с помощью View:
# class ProductDetailsView(View):
#     def get(self, request: HttpRequest, pk: int) -> HttpResponse:
#         # product = Product.objects.get(pk=pk) # выведет ошибку сервера если PK не будет найден
#         product = get_object_or_404(Product, pk=pk) # позволяет вывести ошибку 404 если PK не найден в базе
#         context = {"product": product}
#         return render(request, "shopapp/product_detail.html", context=context)


# рациональнее вывесли детальное описание с помощью DetailView:
class ProductDetailView(DetailView):
    template_name = 'shopapp/product_detail.html'  # указываем шаблон
    # model = Product  # указываем модель, сущности которой будут вытащены из БД (автоматически и все)
    queryset = Product.objects.prefetch_related("images") # для загрузки всех изображений
    context_object_name = "product"  # указываем имя для доступа к вытащенным сущностям (указывается в шаблоне).
    # При этом нет необходимости использовать get_object_or_404 т.к. тут это делается автоматически.


# создадим список с помощью TemplateView. Он работает напрямую с шаблонами
# и явл. наследником класса View:
# class ProductListView(TemplateView):
#     template_name = 'shopapp/products-list.html' # указываем шаблон
#
#     def get_context_data(self, **kwargs): # указываем продукты, рендеринг же происходит в родительском классе
#         context = super().get_context_data(**kwargs)
#         context["products"] = Product.objects.all()
#         return context


# products_list правильнее создать с помощью  ListView:
class ProductListView(ListView):
    template_name = 'shopapp/products-list.html'  # указываем шаблон
    # model = Product  # указываем модель, сущности которой будут вытащены из БД (автоматически и все)
    context_object_name = "products"  # указываем имя для доступа к вытащенным сущностям (указывается в шаблоне)
    queryset = Product.objects.filter(archived=False)  # выведет только не архивированные записи


# создаем продукт с помощью CreateView, шаблоном будет product_form, т.к.
class ProductCreateView(CreateView):
    # UserPassesTestMixin позволяет создать свою функцию для проверки:
    # def test_func(self) -> bool:
    #     return self.request.user.is_superuser

    # def form_valid(self, form):
    #     instance = form.save(commit=False)
    #     instance.created_by = self.request.user
    #     instance.save()
    #     return super().form_valid(form)

    model = Product  # указываем какую модель из model.py создавать
    fields = "name", "price", "description", "discount", "preview",  # указываем запрашиваемые поля из модели
    # form_class = GroupForm -- если описана форма в forms, то можно указать её, тогда fields не надо.
    success_url = reverse_lazy("shopapp:products_list")  # указываем куда перенапавить после создания продукта


# для обновления имеющегося продукта:
class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product  # указываем какую модель из model.py редактируем

    def test_func(self):
        # если суперюзер, либо есть разрешение, либо автор продукта - можно редактировать.
        if self.request.user.is_superuser:
            return True

        self.object = self.get_object()

        has_edit_perm = self.request.user.has_perm("shopapp.change_product")
        created_by_current_user = self.object.created_by == self.request.user
        return has_edit_perm and created_by_current_user


    # fields = "name", "price", "description", "discount", "preview", # указываем доступные к редактированию поля из модели
    template_name_suffix = "_update_form"  # по умолчанию класс использует шаблон как в ProductCreateView,
                                        # что бы использовать иной шаблон укажем его окончание

    form_class = ProductForm # вместо поля fields укажем какую форму использовать при обработке запроса

    # для перехода обратно в детали конкретного продукта нужен pk
    # , но pk через reverse_lazy не доступен, а reverse используется только через функцию
    def get_success_url(self):
        return reverse(
            "shopapp:product_detail",
            kwargs={"pk": self.object.pk}
        )

    # т.к. форме было добавлено новое поле - требуется переопределить метод класса
    def form_valid(self, form):
        response = super().form_valid(form) # сначала выполним метод в стандартном виде
        for image in form.files.getlist("images"): # пербериаем загруженные изображения
            ProductImage.objects.create(product=self.object, image=image) # создаем объекты изображений в БД

        return response



# для "софт" удаления сущностей:
class ProductDeleteView(DeleteView):  # template: product_confirm_delete
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


# 2 переходим из views и прописываем функцию на основе параметров в тесте
class ProductsExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by('pk').all()
        products_data= [
            {'pk': product.pk, 'name': product.name, 'price': product.price, 'archived': product.archived}
            for product in products
            ]
        return JsonResponse({'products': products_data}) # "products" продиктовано тестом


# ________________________From Orders:________________________


class OrdersListView(LoginRequiredMixin, ListView):
    # LoginRequiredMixin ограничивает доступ к VIEW-классу со стороны не аутентифицированных пользователей.

    # укажем queryset вместо template_name т.к. тут есть связи с другими сущностями.
    # При этом шаблон следует переименовать по принципу: модель_структура.html (order_list.html)
    queryset = (
        Order.objects.
        select_related("user").
        prefetch_related("products")
    )
    # context_object_name = "products"  -- либо можно указать в шаблоне object_list


class OrderDetailViev(PermissionRequiredMixin, DetailView):
    # PermissionRequiredMixin позволяет задать список разрешений, с которыми доступен этот класс.
    permission_required = ["shopapp.view_order"]

    queryset = (
        Order.objects.
        select_related("user").
        prefetch_related("products")
    )


class OrderCreateView(CreateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    success_url = reverse_lazy("shopapp:orders_list")


class OrderUpdateView(UpdateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:order_detail",
            kwargs={"pk": self.object.pk}
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")


# __________homework m10__________
class OrdersExportView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by('pk').all()
        orders_data = [
            {'pk': order.pk, 'delivery_address': order.delivery_address,
             'promocode': order.promocode, 'user_id': order.user_id }
            for order in orders
        ]
        return JsonResponse({'orders': orders_data})
