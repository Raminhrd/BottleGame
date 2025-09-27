from django.urls import path
from user_app.views import *


urlpatterns = [
    path('profile-admin', UserProfileView.as_view()),
    path('profile/<str:pk>', UserProfileDetailView.as_view()),
    path('message', MessageListView.as_view()),
    path('message-detail/<str:pk>', MessageDetailView.as_view()),
    path('sea-list', SeaListView.as_view()),
    path('message-purchase/<int:pk>', MessagePurcaseView.as_view()),
    path('add-friend', AddFriendView.as_view()),
    path('friend-list', FriendListView.as_view()),
]