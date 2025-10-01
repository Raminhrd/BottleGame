from django.urls import path
from admin_app.views import BanUserView


urlpatterns = [
    path('ban-user', BanUserView.as_view()),
]