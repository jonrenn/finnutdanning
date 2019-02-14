from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import StudentCreationForm
from .models import Student


class Profile(LoginRequiredMixin, generic.DetailView):
    model = Student
    slug_field = 'username'
    template_name = 'registration/profile.html'


def redirect_to_profile(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user)
    else:
        return redirect('login')


class Register(generic.CreateView):
    form_class = StudentCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'