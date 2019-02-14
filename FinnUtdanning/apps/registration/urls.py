from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView

from apps.registration import views

urlpatterns = [
    url(r'^$', views.redirect_to_profile, name='redirect_to_profile'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^register$', views.Register.as_view(), name='register'),
    url(r'^(?P<slug>[\w.@+-]+)$', views.Profile.as_view(), name='profile'),
]
