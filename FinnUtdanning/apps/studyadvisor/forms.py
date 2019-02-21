from django import forms
from django.forms import widgets
from .models import Studieforslag, Interesser, Studier

class StudieforslagForm(forms.ModelForm):
    class Meta:
        model = Studieforslag
        fields = []

    interesser = forms.ModelMultipleChoiceField(queryset=Interesser.objects.all().order_by('navn'), widget=forms.SelectMultiple(attrs={
        'class' : 'fitContent',
        'style' : 'height:200px;'
    }), required=True)
