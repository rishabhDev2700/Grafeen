from django.urls import path
from account.views import *

app_name = "account"
urlpatterns = [
    path("", user_signin, name="sign-up"),
    path("update-password/", password_update, name="password-update"),
    path("update-user/", user_update, name="user-update"),
    path("redirect", redirected, name="google-redirect"),
    path("logout/", logout_user, name="sign-out"),
]
