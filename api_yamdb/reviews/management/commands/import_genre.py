from django.core.management.base import BaseCommand
from reviews.models import Genre
import csv


class Command(BaseCommand):
    help = 'Загружает файлы genre.csv в базу данных'

    def handle(self, *args, **kwargs):
        file_path = 'static/data/genre.csv'
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                genre, created = Genre.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
                if created:
                    print(f"Создан жанр: {genre.name}")
                else:
                    print(f"Жанр уже существует: {genre.name}")
