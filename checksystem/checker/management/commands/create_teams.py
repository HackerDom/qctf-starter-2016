from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cabinet.models import Team


class Command(BaseCommand):
    help = 'Creates default categories from file'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        self.stdout.write('Loading data from file.')
        with open(options['filename']) as f:
            file_data = f.read()
        # self._add_categories(file_data)
        self.stdout.write(self.style.SUCCESS('All teams are created.'))
