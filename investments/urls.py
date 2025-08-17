# investments/urls.py
from django.urls import path
from .views import investment_view

urlpatterns = [
    path("", investment_view, name="investment"),
]

