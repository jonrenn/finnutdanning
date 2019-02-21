from django.db import models
from FinnUtdanning import settings

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
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    studier = models.ManyToManyField(Studier, through='RelevantStudie')
    interesser = models.ManyToManyField(Interesser)

    class Meta:
        verbose_name_plural = "Studieforslag"

class RelevantStudie(models.Model):
    studieforslag = models.ForeignKey(Studieforslag, on_delete=models.CASCADE)
    studie = models.ForeignKey(Studier, on_delete=models.CASCADE)
    relevans = models.IntegerField(default=0)
