from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.forms import SetPasswordForm
from account.forms import AccountChangeForm
from account.models import User
from config import settings


# Create your views here.
def user_signin(request):
    return render(request, "account/signin.html")


@login_required
def password_update(request):
    if request.method == "POST":
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            messages.success(request, "Password set successfully")
            email = request.user.email
            form.save()
            user = User.objects.get(email=email)
            login(request, user)
            return redirect("account:user-update")
        else:
            messages.error(request, "Unable to set password")
    form = SetPasswordForm(user=request.user)
    return render(request, "account/update.html", {"form": form})


@login_required
def user_update(request):
    if request.method == "POST":
        form = AccountChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            messages.success(request, "Updated User Successfully")
            form.save()
            return redirect("store:explore")
        else:
            messages.error(request, "Unable to update User")
    form = AccountChangeForm(instance=request.user)
    return render(request, "account/update.html", {"form": form})


@csrf_exempt
def redirected(request):
    token = request.POST["credential"]
    try:
        data = id_token.verify_oauth2_token(
            token, requests.Request(), settings.GOOGLE_OAUTH_CLIENT_ID
        )
    except Exception as e:
        messages.error(request, f"Unable to sign-in {e}")
        print(e)
        return redirect("account:sign-up")
    user, created = User.objects.get_or_create(
        email=data["email"], defaults={"full_name": data["name"]}
    )
    login(request, user)
    if created:
        return redirect("account:password-update")
    messages.success(request,"Logged in successfully")
    return redirect("store:explore")


def my_account(request):
    context = {}
    return render(request, "account/my-account.html", context=context)



def logout_user(request):
    logout(request)
    messages.success(request, "User logged out successfully")
    return redirect("account:sign-up")
