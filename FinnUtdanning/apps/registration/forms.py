from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Student


class StudentCreationForm(UserCreationForm):
    class Meta:
        email = forms.EmailField(required=True, help_text="Noe")
        model = Student
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
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