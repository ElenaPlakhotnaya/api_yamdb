from django.core.management.base import BaseCommand
from reviews.models import Title, Category
import csv

class Command(BaseCommand):
    help = 'Загружает файлы titles.csv в базу данных'
    def handle(self, *args, **kwargs):
        file_path = 'static/data/titles.csv'
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                title, created = Title.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(id=row['category']),
                )
                if created:
                    print(f"Создано произведение: {title.name}")
                else:
                    print(f"Произведение уже существует: {title.name}")