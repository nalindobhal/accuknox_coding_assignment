from django.urls import path
from . import views
urlpatterns = [
    path('search/', views.search_user, name='search_user'),
    path('friends/', views.get_friends_list, name='get_friends_list'),
    path('friend_requests/', views.get_friends_request_list, name='get_friends_request_list'),
    path('friend_requests/add/', views.send_friend_request, name='send_friend_request'),
    path('friend_requests/accept/', views.accept_friend_request, name='accept_friend_request'),
]