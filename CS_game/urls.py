from django.urls import path
from .views import CS_game_view

app_name = "CS_game"

urlpatterns = [
    path('', CS_game_view, name='CS_game')
]
