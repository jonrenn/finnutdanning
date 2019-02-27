"""FinnUtdanning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from apps.api.views import aboutpage
from apps.studyadvisor.views import frontpage, nyInteresse, nyttStudie, endre, endreInteresse, endreStudie, slettInteresse, slettStudie

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', frontpage, name='home'),
    url(r'^studieforslag/$', frontpage, name='studieforslag'),
    url(r'^nyInteresse/$', nyInteresse, name='nyInteresse'),
    url(r'^nyttStudie/$', nyttStudie, name='nyttStudie'),
    url(r'^endre/$', endre, name='endre'),
    url(r'^endre/interesse/(?P<id>\d+)/$', endreInteresse, name='endreInteresse'),
    url(r'^endre/studie/(?P<id>\d+)/$', endreStudie, name='endreStudie'),
    url(r'^endre/interesse/slett/(?P<id>\d+)/$', slettInteresse, name='slettInteresse'),
    url(r'^endre/studie/slett/(?P<id>\d+)/$', slettStudie, name='slettStudie'),
    url(r'^bruker/', include('apps.registration.urls'), name='accounts'),
    url(r'^om/$', aboutpage, name='about'),
]
