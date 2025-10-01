from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.utils import timezone
from datetime import timedelta
from Bottle.user_app.models import UserProfile


class BanUserView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data.get("user_id")
            days = int(request.data.get("days", 0))

            if not user_id:
                return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            # گرفتن پروفایل کاربر
            profile = UserProfile.objects.get(id=user_id)

            # حالت‌های مختلف
            if days == 0:
                # بن دائمی
                profile.is_ban = True
                profile.ban_until = None
                msg = "User permanently banned"
            elif days > 0:
                # بن موقت
                profile.is_ban = False
                profile.ban_until = timezone.now() + timedelta(days=days)
                msg = f"User banned for {days} days"
            else:
                # آن‌بَن
                profile.is_ban = False
                profile.ban_until = None
                msg = "User unbanned"

            profile.save()

            return Response(
                {
                    "msg": msg,
                    "user_id": profile.id,
                    "is_ban": profile.is_ban,
                    "ban_until": profile.ban_until,
                },
                status=status.HTTP_200_OK,
            )

        except UserProfile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)











