from django import forms
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


def register(request):
    if request.user.is_authenticated:
        return redirect("customer_profile")

    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("customer_profile")

    return render(request, "customers/register.html", {"form": form})


class CustomerLoginView(LoginView):
    template_name = "customers/login.html"
    redirect_authenticated_user = True


@require_POST
def customer_logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect("home")


@login_required
def customer_profile(request):
    return render(request, "customers/profile.html")
