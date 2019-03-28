from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import StudentCreationForm, StudentChangeForm
from .models import Student


class Profile(LoginRequiredMixin, generic.DetailView):
    model = Student
    slug_field = 'username'
    template_name = 'registration/profile.html'


def redirect_to_profile(request):
    if request.user.is_authenticated:
        return redirect('home', request.user)
    else:
        return redirect('login')


class Register(generic.CreateView):
    form_class = StudentCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


class EditProfile(generic.UpdateView):
    model = Student
    slug_field = 'username'
    template_name = 'registration/profile_form.html'
    form_class = StudentChangeForm

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and self.get_object() == request.user):
            return redirect_to_login(request.get_full_path())
        return super(EditProfile, self).dispatch(
            request, *args, **kwargs)
