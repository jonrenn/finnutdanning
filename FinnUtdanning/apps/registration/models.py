import os
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.urls import reverse

def user_folder(instance, filename):
    return os.path.join('users', instance.username, filename)


class CaseInsensitiveUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class Student(AbstractUser):
    middle_name = models.CharField(max_length=50, blank=True, verbose_name='Mellomnavn')
    objects = CaseInsensitiveUserManager()

    def get_full_name(self):
        if self.middle_name:
            first_name = self.first_name + ' ' + self.middle_name
        else:
            first_name = self.first_name
        if first_name == "" and self.last_name == "":
            return self.username
        return first_name + ' ' + self.last_name

    full_name = property(get_full_name)

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.username})

    def getImage(self):
        if self.is_staff:
            return 'placeholder-profile.png'
        elif self.groups.all().filter(name='veileder').exists():
            return 'placeholder-profile.png'
        else:
            return 'placeholder-profile.png'
