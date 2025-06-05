from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Show BASE_DIR and STATIC_ROOT for debugging static files setup.'

    def handle(self, *args, **kwargs):
        self.stdout.write(f'BASE_DIR: {settings.BASE_DIR}')
        self.stdout.write(f'STATIC_ROOT: {settings.STATIC_ROOT}')
        self.stdout.write(f'STATICFILES_DIRS: {settings.STATICFILES_DIRS}') 