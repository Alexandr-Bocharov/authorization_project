# Generated by Django 4.2 on 2025-01-16 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_phone"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="invite_code",
            field=models.CharField(
                blank="True", max_length=6, null="True", verbose_name="инвайт-код"
            ),
            preserve_default="True",
        ),
    ]
