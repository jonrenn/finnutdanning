from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', chatView, name='chats'),
    url(r'^(?P<pk>[0-9]+)$', loadChat, name='chat'),
    url(r'^feedback$', sendFeedback, name='feedback'),
    url(r'^ask$', askAdvisor, name='ask'),
    url(r'^all$', messageAll, name='all'),
    url(r'^advisor$', advisorChatView, name='advisorChats'),
    url(r'^advisor/(?P<pk>[0-9]+)$', loadAdvisorChat, name='advisorChat'),
    url(r'^admin$', adminChatView, name='adminChats'),
    url(r'^admin/(?P<pk>[0-9]+)$', loadAdminChat, name='adminChat'),
    url(r'^admin/ask$', askAdmin, name='askAdmin'),
]
