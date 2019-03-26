from django.shortcuts import render, redirect, get_object_or_404
from .forms import SendMessageForm
from .models import Message, Chat
from apps.registration.models import Student
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View


def chatView(request):
    context = getChats(request)
    return render(request, "chat/chat.html", context)


def getChats(request):
    user = request.user
    chats = Chat.objects.filter(participents=user).order_by('-last_message__sent_at')
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
    if request.method == "POST":
        form = SendMessageForm(request.POST)
        if form.is_valid():
            send = form.save(commit=False)
            send.from_user = request.user
            send.to_chat = Chat.objects.filter(id=pk).first()
            send.message = form.cleaned_data['message']
            send.save()
            updateChats()
        return redirect('chat', pk)
    context = getChats(request)
    chat = Chat.objects.all().filter(id=pk).first()
    messages = Message.objects.filter(to_chat=chat)
    user = request.user
    alle = Student.objects.filter(username='Alle').first()
    check = [user, alle]
    form = SendMessageForm(request.POST)
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
        'messages': messages,
        'form': form,
    })
    return render(request, "chat/chat.html", context)


def updateChats():
    for chat in Chat.objects.all():
        chat.messages.set(Message.objects.filter(to_chat = chat))
        chat.last_message = chat.messages.last()