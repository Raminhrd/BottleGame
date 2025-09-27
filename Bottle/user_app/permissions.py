from rest_framework.permissions import BasePermission
from user_app.models import UserProfile

class IsNotBanUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        profile = UserProfile.objects.get(user=user)
        if profile.is_ban:
            return False
        else: 
            return True