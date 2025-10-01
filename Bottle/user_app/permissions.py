from rest_framework.permissions import BasePermission
from user_app.models import UserProfile
from datetime import timedelta
from django.utils import timezone

class IsNotBanUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        profile = UserProfile.objects.get(user=user)
        if profile.is_ban:
            return False
        if profile.ban_until is None:
            return True
        if profile.ban_until < timezone.now() :
            return True

        return False