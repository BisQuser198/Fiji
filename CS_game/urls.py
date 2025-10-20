from django.urls import path
from .views import CS_game_view, CS_game_view2

app_name = "CS_game"

urlpatterns = [
    path('', CS_game_view, name='CS_game'),
    path('v2', CS_game_view2, name='CS_game2'),
]
