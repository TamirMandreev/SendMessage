# Generated by Django 4.2.2 on 2025-03-26 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dispatcher", "0009_attempttomailing"),
    ]

    operations = [
        migrations.AddField(
            model_name="attempttomailing",
            name="sent_messages_count",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
