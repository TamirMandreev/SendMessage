# Generated by Django 4.2.2 on 2025-03-28 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_user_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="country",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Страна"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="users/photo", verbose_name="Аватар"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="phone",
            field=models.CharField(
                blank=True, max_length=35, null=True, verbose_name="Телефон"
            ),
        ),
    ]
