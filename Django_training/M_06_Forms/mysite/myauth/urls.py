from django.contrib.auth.views import LoginView
from django.urls import path
from .views import (
    get_cookie_view,
    set_cookie_view,
    set_session_view,
    get_session_view,
    MyLogoutView,
    AboutMyView,
    RegisterView,
    FooBarView,
    ProfileUpdateView, ProfilesListView,
)

app_name = "myauth"

# /myauth/...:

urlpatterns = [
    path("login/",
         LoginView.as_view(
             template_name="myauth/login.html",
             redirect_authenticated_user=True
         ),
         name="login"),
    path("about_me/<int:pk>/", AboutMyView.as_view(), name="about_me"),
    path("about_me/<int:pk>/update/", ProfileUpdateView.as_view(), name="profile_update"),
    path("profiles/", ProfilesListView.as_view(), name="profiles"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("cookie/get/", get_cookie_view, name="cookie_get"),
    path("cookie/set/", set_cookie_view, name="cookie_set"),
    path("session/set", set_session_view, name="session_set"),
    path("session/get", get_session_view, name="session_get"),
    path("foo_bar", FooBarView.as_view(), name="foo_bar")
]

