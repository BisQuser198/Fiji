# docxcloner/urls.py
from django.urls import path
from .views import clone_view

urlpatterns = [
    path("", clone_view, name="clone_view"),
]
