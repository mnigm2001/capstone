import json
from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
from pill_vault.serializers import ItemSerializer  # adjust the import path as necessary

class Command(BaseCommand):
    help = 'Imports data from a JSON file to the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the JSON file containing the data')

    def handle(self, *args, **options):
        file_path = options['file_path']
        if not Path(file_path).is_file():
            raise CommandError('File "{}" does not exist.'.format(file_path))

        with open(file_path, 'r') as file:
            data = json.load(file)
            # {'Image': 'https://www.drugs.com/images/pills/fio/GMK02760/desmopressin-acetate.JPG', 'Link': 'https://www.drugs.com/mtm/desmopressin.html', 'Strength': '0.2 mg', 'Imprint': 'I', 'Color': 'White', 'Shape': 'Round'}
            # current format data = {'name': {Image: '', Link: '', Strength: '', Imprint: '', Color: '', Shape: ''}, 'name': {Image: '', Link: '', Strength: '', Imprint: '', Color: '', Shape: ''}}
            # new format data = {'name': '', 'Image': '', 'Link': '', 'Strength': '', 'Imprint': '', 'Color': '', 'Shape': ''}
            data = {name: {**{'name': name}, **pill_data} for name, pill_data in data.items()}
            # remove image and link from the data
            for pill in data.values():
                pill.pop('Image')
                pill.pop('Link')
            # make all key names lowercase
            data = list(data.values())
            data = [{k.lower(): v for k, v in pill.items()} for pill in data]
            print(data)

            if isinstance(data, list):  # Expecting a list of items
                serializer = ItemSerializer(data=data, many=True)
            else:
                serializer = ItemSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                self.stdout.write(self.style.SUCCESS('Successfully imported data from "{}"'.format(file_path)))
            else:
                errors = serializer.errors
                raise CommandError(f'Error importing data: {errors}')
