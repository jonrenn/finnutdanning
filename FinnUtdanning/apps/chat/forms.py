from django import forms
from django.forms import widgets
from apps.registration.models import Student
from .models import Chat, Message


class SendMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']

        message = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'write_msg',
            'placeholder': '"Type a message"',
        }), required=True)


class CreateNewChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['participents']
        labels = {'participents': 'Send Til'}

        participents = forms.ModelMultipleChoiceField(queryset=Student.objects.all().order_by('full_name'),
                                                      widget=forms.SelectMultiple(attrs={
                                                          'class': 'fitContent',
                                                          'style': 'height:200px;'
                                                      }), required=True)


class AskAdvisorForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['participents']
        labels = {'participents': 'Send Til'}

        participents = forms.ModelMultipleChoiceField(queryset=Student.objects.all().order_by('full_name'),
                                                      widget=forms.SelectMultiple(attrs={
                                                          'class': 'fitContent',
                                                          'style': 'height:200px;'
                                                      }), required=True)
