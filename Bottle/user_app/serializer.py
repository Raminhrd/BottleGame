from rest_framework.serializers import ModelSerializer, StringRelatedField
from user_app.models import *



class UserProfileListSerializer(ModelSerializer):
    user = StringRelatedField()
    class Meta:
        model = UserProfile
        fields = ['user', 'coins', 'is_active']

    
class UserProfileRetrieveUpdateDetsroyserializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'coins', 'is_active']


class MessageListCreateSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields  = ['id', 'receiver', 'text_message']


class MesssageRetrieveUpdateDetsroySerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'text_message']

    
class SeaListCreateSerializer(ModelSerializer):
    class Meta:
        model = Sea
        fields = '__all__'


class SeaListCreateRetrieveUpdateDetsroySerializer(ModelSerializer):
    class Meta:
        model = Sea
        fields = '__all__'


class MessagePurchaseSerializer(ModelSerializer):
    class Meta:
        model = MessagePurchase
        fields = '__all__'


class FriendListCreateSerializer(ModelSerializer):
    owner = StringRelatedField()
    friend = StringRelatedField(many=True)

    class Meta:
        model = FriendList
        fields = '__all__' 


class FriendListRetrieveUpdateDetsroySerializer(ModelSerializer):
    class Meta: 
        model = FriendList
        fileds = '__all__'


class NotificationList(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'