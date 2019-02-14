from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Student


class StudentCreationForm(UserCreationForm):
    class Meta:
        model = Student
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )

class StudentChangeForm(UserChangeForm):
    class Meta:
        model = Student
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'email',
        )