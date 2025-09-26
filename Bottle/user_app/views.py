from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from user_app.serializer import *
import random
from user_app.models import UserProfile, Sea

class UserProfileView(ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer


class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileRetrieveUpdateDetsroyserializer

    def get_permissions(self):
        
        if self.request.method == 'DELETE':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class MessageListView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
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
    permission_classes = [permissions.IsAuthenticated]
    queryset = Message.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff :
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)
    

class SeaListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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
    

class FriendListView(ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = FriendListCreateSerializer


class FriendDetailView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = FriendListRetrieveUpdateDetsroySerializer


class NotificationListView(ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = NotificationList