from django.db import models
from django.utils import timezone
from apps.registration.models import Student


class Message(models.Model):
    #subject = models.Charfield('Subject: ', max_lenght=120)
    sent_at = models.DateTimeField(default=timezone.now())
    from_user = models.ForeignKey(Student)
    to_user = models.ManyToManyField(Student)
    message = models.CharField(max_length=500, blank=False)

