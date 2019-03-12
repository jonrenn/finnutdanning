from django.db import models
from django.utils import timezone
from apps.registration.models import Student


class Message(models.Model):
    #subject = models.Charfield('Subject: ', max_lenght=120)
    sent_at = models.DateTimeField(default=timezone.now())
    from_user = models.ForeignKey(Student)
    to_chat = models.ForeignKey('Chat', related_name='+')
    message = models.CharField(max_length=500, blank=False)

class Chat(models.Model):
    participents = models.ManyToManyField(Student)
    messages = models.ManyToManyField(Message)