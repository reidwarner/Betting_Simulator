from django.urls import path
from . import views


urlpatterns = [
    path('<str:league>', views.simulator, name='simulator'),
    path('game_details/<int:id>', views.game_details, name='game_details'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
]