# Generated by Django 2.1.1 on 2019-02-20 21:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studyadvisor', '0002_auto_20190220_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studieforslag',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]