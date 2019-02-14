from django.shortcuts import render


def frontpage(request):
    return render(request, "frontpage.html")

def aboutpage(request):
    return render(request, "about.html")