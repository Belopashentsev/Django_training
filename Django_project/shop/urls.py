from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from shop import settings

urlpatterns = [
    path("", include("mainapp.urls", namespace="main")),
    path("auth/", include("authapp.urls", namespace="auth")),
    path("basket/", include("basketapp.urls", namespace="basket")),
    path("my/admin/", include("adminapp.urls", namespace="my_admin")),
    path("orders/", include("ordersapp.urls", namespace="orders")),
    path("social/", include("social_django.urls", namespace="social")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    # import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
