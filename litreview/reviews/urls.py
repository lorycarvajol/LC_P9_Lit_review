from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path(
        "accounts/", include("django.contrib.auth.urls")
    ),  # Inclure les URLs d'authentification
]
