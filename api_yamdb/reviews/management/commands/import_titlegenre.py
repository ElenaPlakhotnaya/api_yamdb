from django.core.management.base import BaseCommand
from reviews.models import TitleGenre
import csv

class Command(BaseCommand):
    help = 'Загружает файлы genre_title.csv в базу данных'
    def handle(self, *args, **kwargs):
        file_path = 'static/data/genre_title.csv'
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                titlegenre, created = TitleGenre.objects.get_or_create(
                    title_id=row['title_id'],
                    genre_id=row['genre_id'],
                )
                if created:
                    print(f"Создан: {titlegenre}")
                else:
                    print(f"Уже существует: {titlegenre}")