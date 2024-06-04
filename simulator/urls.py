from django.urls import path
from . import views


urlpatterns = [
    path('games/<str:league>/', views.simulator, name='simulator'),
    path('games/<str:league>/details/<str:team_home>/', views.game_details, name='details'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
]