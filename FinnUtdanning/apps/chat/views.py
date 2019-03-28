from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from .forms import SendMessageForm
from .models import Message, Chat
from apps.registration.models import Student
from apps.studyadvisor.views import send_fargetema
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

    context = {
        'user': user,
        'chats': chats,
        'allChat': allChat,
        'chat': None,
    }
    send_fargetema(request, context)
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
        chat.messages.set(Message.objects.filter(to_chat=chat))
        chat.last_message = chat.messages.last()


def sendFeedback(request):
    if request.method == "POST":
        form = SendMessageForm(request.POST)
        if form.is_valid():
            user = request.user
            if not user.is_authenticated:
                user = Student.objects.filter(username='Anonym').first()
            admin = Student.objects.filter(username='Admin').first()
            chat = Chat.objects.create()
            chat.participents.set([admin, user])

            send = form.save(commit=False)
            send.from_user = user
            send.to_chat = chat
            send.message = form.cleaned_data['message']
            send.save()
            updateChats()
        return redirect('home')
    form = SendMessageForm(request.POST)
    context = {
        'form': form,
    }
    send_fargetema(request, context)
    return render(request, "chat/sendFeedback.html", context)


def askAdvisor(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            form = SendMessageForm(request.POST)
            if form.is_valid():
                veileder = Student.objects.filter(username='Veileder').first()
                chat = Chat.objects.create()
                chat.participents.set([veileder, user])
                pk = chat.id
                send = form.save(commit=False)
                send.from_user = user
                send.to_chat = chat
                send.message = form.cleaned_data['message']
                send.save()
                updateChats()
            return redirect('chat', pk)
        form = SendMessageForm(request.POST)
        context = {
            'form': form,
        }
        send_fargetema(request, context)
        return render(request, "chat/askAdvisor.html", context)
    return redirect('home')


def messageAll(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            form = SendMessageForm(request.POST)
            if form.is_valid():
                alle = Student.objects.filter(username='Alle').first()
                admin = Student.objects.filter(username='Admin').first()
                chat = Chat.objects.create()
                chat.participents.set([alle])
                pk = chat.id
                send = form.save(commit=False)
                send.from_user = admin
                send.to_chat = chat
                send.message = form.cleaned_data['message']
                send.save()
                updateChats()
            return redirect('advisorChat', pk)
        form = SendMessageForm(request.POST)
        context = {
            'form': form,
        }
        send_fargetema(request, context)
        return render(request, "chat/messageAll.html", context)
    return redirect('home')


def advisorChatView(request):
    context = getAdvisorChats(request)
    return render(request, "chat/AdvisorInbox.html", context)


def getAdvisorChats(request):
    user = request.user
    if user.is_staff or user.groups.all().filter(name='veileder').exists():
        chats = Chat.objects.filter(participents=user).order_by('-last_message__sent_at')
        alle = Student.objects.filter(username='Alle')
        allChat = Chat.objects.filter(participents__in=alle)
        veileder = Student.objects.filter(username='Veileder')
        veilederChats = Chat.objects.filter(participents__in=veileder)
        assignedChats = (veilederChats.annotate(num_part=Count('participents'))).filter(num_part__gt=2)
        yourAssigned = veilederChats.filter(participents__in=Student.objects.filter(username=user.username))
        unassignedChats = (veilederChats.annotate(num_part=Count('participents'))).filter(num_part__gt=0).exclude(
            num_part__gt=2)
        admin = Student.objects.filter(username='Admin')
        chatsWithAdmin = Chat.objects.filter(participents__in=admin and Student.objects.filter(username=user.username))

        context = {
            'user': user,
            'chats': chats,
            'allChat': allChat,
            'unassignedChats': unassignedChats,
            'assignedChats': assignedChats,
            'yourAssigned': yourAssigned,
            'chatsWithAdmin': chatsWithAdmin,
            'chat': None,
        }
        send_fargetema(request, context)
        return context
    return redirect('chats')


def loadAdvisorChat(request, pk):
    chat = Chat.objects.all().filter(id=pk).first()
    user = request.user
    if user.is_staff or user.groups.all().filter(name='veileder').exists():
        if request.method == "POST":
            form = SendMessageForm(request.POST)
            if form.is_valid():
                if not user in chat.participents:
                    chat.participents.add(user)
                send = form.save(commit=False)
                send.from_user = user
                send.to_chat = Chat.objects.filter(id=pk).first()
                send.message = form.cleaned_data['message']
                send.save()
                updateChats()
            return redirect('advisorChat', pk)
        context = getChats(request)
        messages = Message.objects.filter(to_chat=chat)
        form = SendMessageForm(request.POST)

        context.update({
            'Chat': chat,
            'messages': messages,
            'form': form,
        })
        return render(request, "chat/AdvisorInbox.html", context)
    return redirect('chats')


def adminChatView(request):
    context = getAdminChats(request)
    return render(request, "chat/AdminInbox.html", context)


def getAdminChats(request):
    user = request.user
    if user.is_staff or user.groups.all().filter(name='veileder').exists():
        chats = Chat.objects.filter(participents=user).order_by('-last_message__sent_at')
        Alle = Student.objects.filter(username='Alle')
        allChat = Chat.objects.filter(participents__in=Alle)
        Veileder = Student.objects.filter(username='Veileder')
        veilederChats = Chat.objects.filter(participents__in=Veileder)
        assignedChats = (veilederChats.objects.annotate(num=Count('participents')).filter(num__gt=2))
        unassignedChats = veilederChats.exclude(assignedChats)

        context = {
            'user': user,
            'chats': chats,
            'allChat': allChat,
            'veilederChats': veilederChats,
            'unassignedChats': unassignedChats,
            'assignedChats': assignedChats,
            'chat': None,
        }
        send_fargetema(request, context)
        return context
    return redirect('chats')


def loadAdminChat(request, pk):
    chat = Chat.objects.all().filter(id=pk).first()
    user = request.user
    if request.method == "POST":
        form = SendMessageForm(request.POST)
        if form.is_valid():
            if not user in chat.participents:
                chat.participents.add(user)
            send = form.save(commit=False)
            send.from_user = user
            send.to_chat = Chat.objects.filter(id=pk).first()
            send.message = form.cleaned_data['message']
            send.save()
            updateChats()
        return redirect('advisorChat', pk)
    context = getChats(request)
    messages = Message.objects.filter(to_chat=chat)
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
