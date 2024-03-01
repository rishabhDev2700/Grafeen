from django.urls import path
from .views import explore

app_name="store"
urlpatterns = [
    path('',explore,name="explore")
]