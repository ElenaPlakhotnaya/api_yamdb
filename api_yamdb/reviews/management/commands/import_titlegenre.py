import csv

from django.core.management.base import BaseCommand

from reviews.models import Genre, Title, TitleGenre


class Command(BaseCommand):
    help = 'Загружает файлы genre_title.csv в базу данных'

    def handle(self, *args, **kwargs):
        file_path = 'static/data/genre_title.csv'
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                titlegenre, created = TitleGenre.objects.get_or_create(
                    title_id=Title.objects.get(pk=row['title_id']),
                    genre_id=Genre.objects.get(pk=row['genre_id']),
                )
                if created:
                    self.stdout.write(f'Создан: {titlegenre}')
                else:
                    self.stdout.write(f'Уже существует: {titlegenre}')
