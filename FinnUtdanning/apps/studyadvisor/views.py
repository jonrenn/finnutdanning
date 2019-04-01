from django.shortcuts import render, redirect, get_object_or_404
from .models import Interesser, Studier, RelevantStudie, Studieforslag, Fargetema
from .forms import StudieforslagForm, EndreInteresseForm, EndreStudieForm, FargetemaForm
from django.contrib.auth.decorators import user_passes_test

def veileder_check(user):
    isVeileder = user.groups.all().filter(name='veileder').exists()
    return isVeileder

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

@user_passes_test(veileder_check, login_url='home', redirect_field_name=None)
def personligFargetema(request):
    gamleFargetema = Fargetema.objects.filter(bruker=request.user)
    if request.method == "POST":
        form = None
        if len(gamleFargetema) > 0:
            form = FargetemaForm(request.POST, instance=gamleFargetema[0])
        else:
            nyttFargetema = Fargetema.objects.create(navbarFarge='#000000', bakgrunnFarge='#000000')
            form = FargetemaForm(request.POST, instance=nyttFargetema)
        if form.is_valid():
            fargetema = form.save(commit=False)
            if request.user.is_authenticated:
                fargetema.bruker = request.user
            fargetema.navbarFarge = form.cleaned_data['navbarFarge']
            fargetema.bakgrunnFarge = form.cleaned_data['bakgrunnFarge']
            fargetema.save()
    form = None
    if len(gamleFargetema) > 0:
        form = FargetemaForm(instance=gamleFargetema[0])
    else:
        form = FargetemaForm()
    context = {
        'form' : form
    }
    send_fargetema(request, context)
    return render(request, "studyadvisor/personligfargetema.html", context)

@user_passes_test(lambda u: u.is_staff, login_url='home', redirect_field_name=None)
def globaltFargetema(request):
    gamleFargetema = Fargetema.objects.filter(bruker=None)
    if request.method == "POST":
        form = None
        if len(gamleFargetema) > 0:
            form = FargetemaForm(request.POST, instance=gamleFargetema[0])
        else:
            nyttFargetema = Fargetema.objects.create(navbarFarge='#000000', bakgrunnFarge='#000000')
            form = FargetemaForm(request.POST, instance=nyttFargetema)
        if form.is_valid():
            fargetema = form.save(commit=False)
            fargetema.bruker = None
            fargetema.navbarFarge = form.cleaned_data['navbarFarge']
            fargetema.bakgrunnFarge = form.cleaned_data['bakgrunnFarge']
            fargetema.save()
    form = None
    if len(gamleFargetema) > 0:
        form = FargetemaForm(instance=gamleFargetema[0])
    else:
        form = FargetemaForm()
    context = {
        'form' : form
    }
    send_fargetema(request, context)
    return render(request, "studyadvisor/globaltfargetema.html", context)

def frontpage(request):
    if request.method == "POST":
        form = StudieforslagForm(request.POST)
        if form.is_valid():
            sf = form.save(commit=False)
            if request.user.is_authenticated:
                sf.student = request.user
            else:
                sf.student = None
            sf = form.save()
            for int in sf.interesser.all():
                i = Interesser.objects.get(pk=int.pk)
                i.popularitet += 1
                i.save()

            for s in Studier.objects.all():
                rel = 0 #   Relevans
                for i in sf.interesser.all():
                    if s.interesser.all().filter(pk=i.pk).exists():
                        rel += 1
                if rel > 0:
                    RelevantStudie.objects.create(studieforslag=sf, studie=s, relevans=rel)
            sf.save()
            context = {
                'studier' : RelevantStudie.objects.all().filter(studieforslag_id=sf.pk).order_by('-relevans'),
                'interesser' : sf.interesser.all().order_by('navn'),
                'popInteresser' : Interesser.objects.all().order_by('-popularitet')[:10]
            }
            send_fargetema(request, context)
            return render(request, "studyadvisor/studieforslag.html", context)

    form = StudieforslagForm()
    context = {
        'form' : form
    }
    send_fargetema(request, context)
    return render(request, "frontpage.html", context)


def prev_searches(request):
    studie_forslag = Studieforslag.objects.all().filter(student=request.user).reverse()
    prev_search = []
    for studieforslag in studie_forslag:
        relevantstudie = RelevantStudie.objects.all().filter(studieforslag=studieforslag).order_by('-relevans')
        prev_search.append([studieforslag,relevantstudie])
    context = {
        'searches': prev_search,
    }
    send_fargetema(request, context)
    return render(request, "studyadvisor/prev_searches.html", context)


@user_passes_test(veileder_check, login_url='home', redirect_field_name=None)
def nyInteresse(request):
    if request.method == "POST":
        form = EndreInteresseForm(request.POST)

        if form.is_valid():
            interesse = form.save(commit=False)
            interesse.navn = form.cleaned_data['navn']
            interesse.save()
            return redirect("endre")
    else:
        form = EndreInteresseForm()
        context = {
            'form' : form
        }
        send_fargetema(request, context)
        return render(request, "studyadvisor/nyinteresse.html", context)


@user_passes_test(veileder_check, login_url='home', redirect_field_name=None)
def nyttStudie(request):
    if request.method == "POST":
        form = EndreStudieForm(request.POST)

        if form.is_valid():
            studie = form.save()
            studie.navn = form.cleaned_data['navn']
            studie.interesser.set(form.cleaned_data['interesser'])
            studie.save()
            return redirect("endre")
    else:
        form = EndreStudieForm()
        context = {
            'form' : form
        }
        send_fargetema(request, context)
        return render(request, "studyadvisor/nystudieretning.html", context)


@user_passes_test(veileder_check, login_url='home', redirect_field_name=None)
def endre(request):
    context = {
        'interesser' : Interesser.objects.all().order_by('navn'),
        'studier' : Studier.objects.all().order_by('navn')
    }
    send_fargetema(request, context)
    return render(request, "studyadvisor/endrestudint.html", context)


@user_passes_test(veileder_check, login_url='home', redirect_field_name=None)
def endreInteresse(request, id):
    interesse = get_object_or_404(Interesser, pk=id)

    if request.method == "POST":
        form = EndreInteresseForm(request.POST, instance=interesse)

        if form.is_valid():
            interesse = form.save(commit=False)
            interesse.navn = form.cleaned_data['navn']
            interesse.save()
            return redirect("endre")
    else:
        form = EndreInteresseForm(instance=interesse)
        context = {
            'form' : form,
            'id' : id
        }
        send_fargetema(request, context)
        return render(request, "studyadvisor/endreinteresse.html", context)


@user_passes_test(veileder_check, login_url='home', redirect_field_name=None)
def endreStudie(request, id):
    studie = get_object_or_404(Studier, pk=id)

    if request.method == "POST":
        form = EndreStudieForm(request.POST, instance=studie)

        if form.is_valid():
            studie = form.save(commit=False)
            studie.navn = form.cleaned_data['navn']
            studie.interesser.set(form.cleaned_data['interesser'])
            studie.save()
            return redirect("endre")
    else:
        form = EndreStudieForm(instance=studie)
        context = {
            'form' : form,
            'id' : id
        }
        send_fargetema(request, context)
        return render(request, "studyadvisor/endrestudie.html", context)


@user_passes_test(veileder_check, login_url='home', redirect_field_name=None)
def slettInteresse(request, id):
    interesse = Interesser.objects.get(id=id)
    interesse.delete()
    return redirect("endre")


@user_passes_test(veileder_check, login_url='home', redirect_field_name=None)
def slettStudie(request, id):
    studie = Studier.objects.get(id=id)
    studie.delete()
    return redirect("endre")
