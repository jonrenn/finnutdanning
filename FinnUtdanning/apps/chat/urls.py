from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', chatView, name='chats'),
    url(r'^(?P<pk>[0-9]+)$', loadChat, name='chat'),
]
