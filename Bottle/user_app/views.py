from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from user_app.serializer import *
import random
from user_app.models import UserProfile, Sea
from user_app.permissions import IsNotBanUser




class UserProfileView(ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer
            

class MessageListView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsNotBanUser]
    queryset = Message.objects.all()
    serializer_class = MessageListCreateSerializer

    def create(self, serializer):
        try:
            serializer = self.get_serializer(data=self.request.data)
            serializer.is_valid(raise_exception=True)
            user = UserProfile.objects.get(user=self.request.user)
            user.pay_coin(10)
            serializer.save(sender=user)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.validated_data, 201, headers=headers)   
        except Exception as e:
            return Response(status=400, data=str(e))   

        
class MessageDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = MesssageRetrieveUpdateDetsroySerializer
    permission_classes = [permissions.IsAuthenticated, IsNotBanUser]
    queryset = Message.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff :
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)
    

class SeaListView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsNotBanUser]

    def get(self, request):
        user = UserProfile.objects.get(user=request.user)
        messages = Message.objects.filter(receiver=None).exclude(sender=user)
        if messages.count()== 0 :
            return Response("no message avaliable")
        message = random.choice(messages)
        message.is_read=True
        message.receiver = user
        message.save()
        return Response(MessageListCreateSerializer(message).data)
    

class MessagePurcaseView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsNotBanUser]

    def post(self, request, pk):
        user = UserProfile.objects.get(user=request.user)

        try:
            message = Message.objects.get(pk=pk)
            if MessagePurchase.objects.filter(user=user, message=message).exists():
                return Response({"receiver": message.receiver.user.username})
            user.pay_coin(30)
            MessagePurchase.objects.create(user=user, message=message)
            return Response({"receiver": message.receiver.user.username})
        
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    
class FriendListView(ListAPIView):
    queryset = FriendList.objects.all()
    serializer_class = FriendListCreateSerializer


class AddFriendView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsNotBanUser]

    def post(self, request, pk=None):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            username = request.data.get("username")
            if not username:
                return Response({"error": "username is required"}, status=400)

            friend = UserProfile.objects.get(user__username=username)
            friend_list, created = FriendList.objects.get_or_create(owner=user_profile)
            if friend_list.friend.filter(id=friend.id).exists():
                return Response({"friend": friend.user.username, "msg": "Already in friend list"})
            user_profile.pay_coin(50)
            friend_list.friend.add(friend)
            return Response({"friend": friend.user.username, "msg": "Friend added successfully"})

        except UserProfile.DoesNotExist:
            return Response({"error": "Friend not found"}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=400)
        

class RemoveFriend(APIView):
    permission_classes = [permissions.IsAuthenticated, IsNotBanUser]

    def post(self, request, pk=None):

        try:
            user_profile = UserProfile.objects.get(user=request.user)
            username = request.data.get("username")
            if not username:
                return Response({"error": "username is required"}, status=400)
            
            friend = UserProfile.objects.get(user__username=username)
            friend_remove = FriendList.objects.get(owner=user_profile)
            if not friend_remove.friend.filter(id=friend.id).exists():
                return Response({"friend": friend.user.username, "msg": "You Do Not Have This Friend  At list"})
            
            friend_remove.friend.remove(friend)
            return Response({"friend": friend.user.username, "msg": "Friend remove successfully"})
        
        except UserProfile.DoesNotExist:
            return Response({"error": "Friend not found"}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=400)
        

class NotificationListView(ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = NotificationList