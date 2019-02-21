from django.shortcuts import render, redirect
from django.db.models import F
from .models import Interesser, Studier, RelevantStudie
from .forms import StudieforslagForm

def frontpage(request):
    if request.method == "POST":
        form = StudieforslagForm(request.POST)
        if form.is_valid():
            sf = form.save(commit=False)
            sf.student = request.user
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
            return render(request, "studieforslag.html", context)

    form = StudieforslagForm()
    context = {
        'form' : form
    }
    return render(request, "frontpage.html", context)
