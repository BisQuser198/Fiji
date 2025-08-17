# dates/urls.py
from django.urls import path
from .views import earliest_dates_view

urlpatterns = [
    path("", earliest_dates_view, name="earliest_dates"),
]
