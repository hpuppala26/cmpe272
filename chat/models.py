from django.db import models

# Create your models here.
class Message(models.Model):
    sender = models.CharField(max_length = 50)
    roomname = models.CharField(max_length = 100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
