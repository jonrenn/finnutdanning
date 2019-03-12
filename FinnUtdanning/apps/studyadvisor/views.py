from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from .models import Interesser, Studier, RelevantStudie, Studieforslag
from .forms import StudieforslagForm, EndreInteresseForm, EndreStudieForm
from django.contrib.auth.decorators import user_passes_test

def veileder_check(user):
    isVeileder = user.groups.all().filter(name='veileder').exists()
    return isVeileder

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
            return render(request, "studyadvisor/studieforslag.html", context)

    form = StudieforslagForm()
    context = {
        'form' : form
    }
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
        return render(request, "studyadvisor/nystudieretning.html", context)


@user_passes_test(veileder_check, login_url='home', redirect_field_name=None)
def endre(request):
    context = {
        'interesser' : Interesser.objects.all().order_by('navn'),
        'studier' : Studier.objects.all().order_by('navn')
    }
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