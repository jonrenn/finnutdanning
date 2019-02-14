from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import redirect_to_login
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import generic

from .forms import StudentForm
from .models import Student, RecoveryMail


class Profile(LoginRequiredMixin, generic.DetailView):
    model = Student
    slug_field = 'username'
    template_name = 'registration/profile.html'


class EditProfile(generic.UpdateView):
    model = Student
    slug_field = 'username'
    template_name = 'registration/profile_form.html'
    form_class = StudentForm

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and self.get_object() == request.user):
            return redirect_to_login(request.get_full_path())
        return super(EditProfile, self).dispatch(
            request, *args, **kwargs)


def redirect_to_profile(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user)
    else:
        return redirect('login')


token_generator = PasswordResetTokenGenerator()


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/home')
    else:
        form = UserCreationForm()

        args= {'form': form}
        return render(request, 'accounts/reg_form.html', args)


def complete_registration(request, uidb64, token):
    UserModel = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    valid = (user is not None and token_generator.check_token(user, token))
    if valid:
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = SetPasswordForm(user)
    else:
        form = None
    return render(request, 'registration/reset_password.html', {'valid': valid, 'form': form})