# Generated by Django 4.2 on 2025-01-18 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_alter_user_phone"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "verbose_name": "пользовательь",
                "verbose_name_plural": "пользователи",
            },
        ),
    ]
