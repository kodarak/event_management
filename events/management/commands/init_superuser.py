from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates a superuser if it does not exist'

    def handle(self, *args, **options):
        if not User.objects.filter(username='root').exists():
            User.objects.create_superuser(
                username='root',
                email='root@example.com',
                password='maga123!@#'
               )
            self.stdout.write(self.style.SUCCESS("Superuser 'root' created."))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser 'root' already exists."))
