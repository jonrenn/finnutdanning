from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import  render, redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import StudentCreationForm, StudentChangeForm
from .models import Student
from apps.studyadvisor.models import Fargetema

def send_fargetema(request, context):
    if request.user.is_authenticated:
        fargetemaPrivat = Fargetema.objects.filter(bruker=request.user)
        if len(fargetemaPrivat) > 0 and fargetemaPrivat[0].brukPersonlig == True:
            context['navbarFarge'] = fargetemaPrivat[0].navbarFarge
            context['bakgrunnFarge'] = fargetemaPrivat[0].bakgrunnFarge
            return
    fargetemaGlobal = Fargetema.objects.filter(bruker=None)
    if len(fargetemaGlobal) > 0 and fargetemaGlobal[0].brukPersonlig == True:
        context['navbarFarge'] = fargetemaGlobal[0].navbarFarge
        context['bakgrunnFarge'] = fargetemaGlobal[0].bakgrunnFarge
    return

class Profile(LoginRequiredMixin, generic.DetailView):
    model = Student
    slug_field = 'username'
    template_name = 'registration/profile.html'


def redirect_to_profile(request):
    if request.user.is_authenticated:
        return redirect('home', request.user)
    else:
        context = {}
        send_fargetema(request, context)
        return render(request, 'login.html', context)


class Register(generic.CreateView):
    form_class = StudentCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'
