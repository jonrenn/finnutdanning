from django.shortcuts import render, redirect, get_object_or_404
from .forms import SendMessageForm
from .models import Message, Chat
from apps.registration.models import Student
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View


class ChatView(TemplateResponseMixin, ContextMixin, View):
    def get(self, request, *args, **kwargs):
        context = getChats(request)
        return self.render_to_response(context)


def chatView(request):
    context = getChats(request)
    return render(request, "chat/chat.html", context)


def sendMessage(request, pk):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            form = SendMessageForm(request.POST)
            if form.is_valid():
                chat_id = request.POST['chat_id']
                text = request.POST['text']
                message = Message(from_user=user, to_chat_id=chat_id, message=text)
                message.save()
    return redirect('chat', pk)


def getChats(request):
    user = request.user
    chats = Chat.objects.filter(participents=user)
    Alle = Student.objects.filter(username='Alle')
    allChat = Chat.objects.filter(participents__in=Alle)
    veilederChats = None

    if user.groups.filter(name='veileder').exists():
        Veileder = Student.objects.filter(username='Veileder')
        veilederChats = Chat.objects.filter(participents__in=Veileder)

    context = {
        'user': user,
        'chats': chats,
        'allChat': allChat,
        'veilederChats': veilederChats,
        'chat': None,
    }
    return context


def loadChat(request, pk):
    context = getChats(request)
    chat = Chat.objects.all().filter(id=pk).first()
    user = request.user
    alle = Student.objects.filter(username='Alle').first()
    check = [user, alle]
    if user.groups.filter(name='veileder').exists():
        veileder = Student.objects.filter(username='Veileder').first()
        check.append(veileder)
    x = 0
    for participent in chat.participents.all():
        if participent in check:
            x = 1
    if x == 0:
        return redirect("chats")

    context.update({
        'Chat': chat,
    })
    return render(request, "chat/chat.html", context)
