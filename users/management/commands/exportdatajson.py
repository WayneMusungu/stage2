import os
import json
from django.core.management.base import BaseCommand
from django.core.serializers import serialize

from organisations.models import Organisation
from users.models import User


class Command(BaseCommand):
    help = 'Export data from models to JSON files'

    def handle(self, *args, **options):
        try:
            # Export User data
            # user_data = serialize('json', User.objects.all())
            # self.write_to_file('users.json', user_data)

            # Export Organisations data
            organisations_data = serialize('json', Organisation.objects.all())
            self.write_to_file('organisations.json', organisations_data)

            self.stdout.write(self.style.SUCCESS('Successfully exported data to JSON files'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to export data: {str(e)}'))

    def write_to_file(self, filename, data):
        file_path = os.path.join('data_exports', filename)  
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(data)
