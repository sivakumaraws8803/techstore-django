from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.CustomerLoginView.as_view(), name="login"),
    path("logout/", views.customer_logout, name="logout"),
    path("profile/", views.customer_profile, name="customer_profile"),
]
