from django.db import models
from ..users.models import User

class Chat(models.Model):
    name = models.CharField(max_length=255)
    chat_status = models.IntegerField()

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type_msg = models.CharField(max_length=50)
    type_location = models.CharField(max_length=50)
    type_ack = models.CharField(max_length=50)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
