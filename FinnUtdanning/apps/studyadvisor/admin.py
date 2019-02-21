from django.contrib import admin

# Register your models here.
from .models import Interesser, Studier, Studieforslag, RelevantStudie

admin.site.register(Interesser)
admin.site.register(Studier)
admin.site.register(Studieforslag)
admin.site.register(RelevantStudie)
