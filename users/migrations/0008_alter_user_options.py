# Generated by Django 4.2 on 2025-01-18 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_alter_user_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "verbose_name": "пользователь",
                "verbose_name_plural": "пользователи",
            },
        ),
    ]
