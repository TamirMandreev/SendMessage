# Generated by Django 4.2.2 on 2025-03-23 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatcher', '0007_alter_message_options_alter_message_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='date_time_end_mailing',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата и время окончания отправки'),
        ),
    ]
