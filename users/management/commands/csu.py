from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            phone='79647666497',
            is_staff=True,
            is_superuser=True,
        )
        user.set_password('1234')
        user.save()
