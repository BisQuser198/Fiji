# docxcloner/urls.py
from django.urls import path
from .views import clone_view

app_name = "clone_files"

urlpatterns = [
    #path("", clone_view, name="clone_view"),
    path("", clone_view, name="clone"),
    # now {% url 'clone_files:form' %} → /clone_files/ (see step 2)
]


