from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=100)
    is_active = models.BooleanField(default=True)
    is_ban = models.BooleanField(default=False)

    def __str__(self):
        if self.user.first_name:
            return self.user.first_name
        else:
            return self.user.get_full_name()
        
    
    def pay_coin(self, coin_number):
        if self.coins >= coin_number:
            self.coins -= coin_number
            self.save()
        else:
            raise ValidationError("Not enought coins!")


class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender_message', null=True, blank=True)
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='receiver_message', null=True, blank=True)
    text_message = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.text_message


class Sea(models.Model):
    Message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='message_sea')

    def __str__(self):
        return self.Message


class FriendList(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='owner_friendlist')
    friend = models.ManyToManyField(UserProfile)

    def __str__(self):
        return f"{self.owner.user.username} is friend {self.friend}"


class Notification(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender_notification')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='receiver_notification')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='message_notification')

    def __str__(self):
        return self.message
