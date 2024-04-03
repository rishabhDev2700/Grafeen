from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse

from django.urls import resolve


class LoginRequiredAccess:
    """All urls starting with the given prefix require the user to be logged in"""

    APP_NAME = 'dashboard'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "Requires the django's authentication middleware"
                " to be installed.")

        user = request.user
        if resolve(request.path).app_name == self.APP_NAME:  # match app_name defined in myapp.urls.py
            if not user.is_authenticated:
                path = request.get_full_path()
                return redirect_to_login(path)
            elif not user.is_superuser:
                return HttpResponse('Not Allowed')

        return self.get_response(request)