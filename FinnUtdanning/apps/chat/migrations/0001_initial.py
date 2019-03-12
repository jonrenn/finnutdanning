# Generated by Django 2.1.7 on 2019-03-12 11:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('message', models.CharField(max_length=500)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('to_chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='chat.Chat')),
            ],
        ),
        migrations.AddField(
            model_name='chat',
            name='messages',
            field=models.ManyToManyField(to='chat.Message'),
        ),
        migrations.AddField(
            model_name='chat',
            name='participents',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
