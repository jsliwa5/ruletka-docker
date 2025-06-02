from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login),
    path('update-balance/', views.update_balance),
    path('history/', views.get_game_history),
    path('get-balance/', views.get_balance),
    path('add-funds/', views.add_funds),
    path('register/', views.register),
    path('logout/', views.user_logout)

]