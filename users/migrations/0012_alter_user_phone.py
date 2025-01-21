# Generated by Django 4.2 on 2025-01-19 12:59

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0011_alter_user_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone",
            field=models.CharField(
                max_length=15,
                unique=True,
                validators=[users.validators.validate_phone],
                verbose_name="номер телефона",
            ),
        ),
    ]
