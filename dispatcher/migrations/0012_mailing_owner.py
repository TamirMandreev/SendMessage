# Generated by Django 4.2.2 on 2025-03-27 07:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dispatcher', '0011_remove_attempttomailing_sent_messages_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mailings', to=settings.AUTH_USER_MODEL),
        ),
    ]
