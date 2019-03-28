from django.db import models
from apps.registration.models import Student

# Create your models here.
class Interesser(models.Model):
    navn = models.CharField(max_length=200)
    popularitet = models.IntegerField(default=0)
    def __str__(self):
        return self.navn
    class Meta:
        verbose_name_plural = "Interesser"

class Studier(models.Model):
    navn = models.CharField(max_length=200)
    interesser = models.ManyToManyField(Interesser)
    def __str__(self):
        return self.navn
    class Meta:
        verbose_name_plural = "Studier"

class Studieforslag(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    studier = models.ManyToManyField(Studier, through='RelevantStudie')
    interesser = models.ManyToManyField(Interesser)

    class Meta:
        verbose_name_plural = "Studieforslag"

class RelevantStudie(models.Model):
    studieforslag = models.ForeignKey(Studieforslag, on_delete=models.CASCADE)
    studie = models.ForeignKey(Studier, on_delete=models.CASCADE)
    relevans = models.IntegerField(default=0)

class Fargetema(models.Model):
    bruker = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    brukPersonlig = models.BooleanField(default=True)
    navbarFarge = models.CharField(max_length=7)
    bakgrunnFarge = models.CharField(max_length=7)
    class Meta:
        verbose_name_plural = "Fargetema"
