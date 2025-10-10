from django.urls import path
from .views import mass_rename

app_name = "file_renamer"

urlpatterns = [
    path('', mass_rename, name='mass_rename'),
]