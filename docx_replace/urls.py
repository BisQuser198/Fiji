# docx_replace/urls.py
from django.urls import path
from .views import replace_view

urlpatterns = [
    path("", replace_view, name="replace_docs"),
]
